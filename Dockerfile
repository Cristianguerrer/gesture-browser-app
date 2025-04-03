FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn

EXPOSE 8000

CMD ["python", "main.py"]
