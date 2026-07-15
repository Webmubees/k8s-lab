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

@app.get("/health")
def health():
    
    raise HTTPException(status_code=500 , detail="Database unavailable")

@app.get("/live")
def live():
    return {"status": "alive"}



READY = True
@app.get("/ready")
def ready():
    if READY:
        return {"status": "ready"}

    raise HTTPException(status_code=503, detail="Not Ready")