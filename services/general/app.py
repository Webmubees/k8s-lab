from fastapi import FastAPI, HTTPException
import socket
import os
import time

app = FastAPI()

# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {
        "service": "General Service",
        "hostname": socket.gethostname(),
        "company": os.getenv("COMPANY"),
        "version": os.getenv("VERSION"),
        "environment": os.getenv("ENVIRONMENT")
    }

# -----------------------------
# Liveness Probe
# -----------------------------
@app.get("/live")
def live():
    return {
        "status": "alive"
    }

# -----------------------------
# Readiness Probe
# -----------------------------
ready = True

@app.get("/ready")
def ready_check():
    if ready:
        return {
            "status": "ready"
        }

    raise HTTPException(
        status_code=503,
        detail="Service Not Ready"
    )

# -----------------------------
# Debug Endpoints
# -----------------------------
@app.post("/debug/not-ready")
def not_ready():
    global ready
    ready = False
    return {
        "status": "Pod is now Not Ready"
    }

@app.post("/debug/ready")
def ready_again():
    global ready
    ready = True
    return {
        "status": "Pod is Ready Again"
    }

# -----------------------------
# CPU Stress Test
# -----------------------------
@app.get("/cpu")
def cpu():
    x = 0

    while True:
        x += 1

# -----------------------------
# Memory Leak (OOMKilled Test)
# -----------------------------
memory_store = []

@app.get("/memory")
def memory_test():

    while True:
        memory_store.append("A" * 1024 * 1024)   # 1 MB

        time.sleep(0.05)