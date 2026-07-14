from fastapi import FastAPI
import socket
import os

app = FastAPI()

@app.get("/")
def home():
    return {
        "Service" : "General Service",
        "hostname" : socket.gethostname(),
        "company" : os.getenv("COMPANY"),
        "version" : os.getenv("VERSION"),
        "environment" : os.getenv("ENVIRONMENT")
    }

@app.get("/health")
def health():
    return {
        "status" : "healthy"
    }