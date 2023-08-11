import uuid
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from redis import Redis
import config


class LongLink(BaseModel):
    link: str

token_to_link = Redis(config.REDIS_HOST, config.REDIS_PORT, 0)
link_to_token = Redis(config.REDIS_HOST, config.REDIS_PORT, 1)
app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://frontend:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(
    prefix = '/api'
)

@router.get("/health")
def health():
    return {"health": "OK"}

@router.post("/")
def create_short_url(long_link: LongLink, expires: bool = True):
    token = None
    if (token := link_to_token.get(long_link.link)):
        token = token.decode()
        return JSONResponse({"short_url": config.SERVICE_ROOT+token}, status_code=208)
    while True: 
        token = uuid.uuid4().hex[:9].upper()
        if not token_to_link.get(token):
            token_to_link.set(token, long_link.link)
            link_to_token.set(long_link.link, token)
            return JSONResponse({"short_url": config.SERVICE_ROOT+token}, status_code=201)


@router.get("/{token:str}")
def redirect(token: str):
    long_link = token_to_link.get(token)
    print(long_link)
    if long_link:
        long_link = long_link.decode()
        if not long_link.startswith('http://') and not long_link.startswith('https://'):
            return RedirectResponse("http://"+long_link)
        return RedirectResponse(long_link)

    return JSONResponse({"message": "No such short link"}, status_code=404)

app.include_router(router)