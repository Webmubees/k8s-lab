from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/")
def home():
    return {
        "Service" : "General Service",
        "hostname" : socket.gethostname(),
        "company" : "k8s-labs",
        "version" : "1.0.0",
        "environment" : "deployment"
    }

@app.get("/health")
def health():
    return {
        "status" : "healthy"
    }