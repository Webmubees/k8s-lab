from fastapi import FastAPI
from fastapi import HTTPException
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


@app.get("/live")
def live():
    return {"status": "alive"}

ready = True

@app.get("/ready")
def ready_check():
    if ready:
        return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Service Not Ready")


@app.post("/debug/not-ready")
def not_ready():
    global ready
    ready = False
    return {"status": "Pod is now Not Ready"}

@app.post("/debug/ready")
def ready_again():
    global ready
    ready = True
    return {"status": "Pod is Ready Again"}