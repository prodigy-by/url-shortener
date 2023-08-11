FROM python:3.10-alpine

WORKDIR /app

COPY . .
RUN pip install -r req.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]