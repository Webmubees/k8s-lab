from fastapi import FastAPI
from fastapi import HTTPException
import socket
import os
import time

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
    while True:
        time.sleep(1)

@app.get("/live")
def live():
    return {"status": "alive"}


READY = True
@app.get("/ready")
def ready():
    if READY:
        return {"status": "ready"}

    raise HTTPException(status_code=503, detail="Not Ready")