import uuid
from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from redis import Redis
import config


class LongLink(BaseModel):
    link: str

redis = Redis(config.REDIS_HOST, config.REDIS_PORT, 0)
app = FastAPI()


@app.post("/")
def create_short_url(long_link: LongLink, expires: bool = True):
    token = None
    while True: 
        token = uuid.uuid4().hex[:9].upper()
        if not redis.get(token):
            redis.set(token, long_link.link)
            return JSONResponse({"short_url": config.SERVICE_ROOT+token}, status_code=201)


@app.get("/{token:str}")
def redirect(token: str):
    long_link = redis.get(token)
    long_link = long_link.decode()
    if long_link:
        return RedirectResponse(long_link)

    return JSONResponse({"message": "No such short link"}, status_code=404)