from fastapi import FastAPI, HTTPException
import socket
import os
import time
from fastapi.responses import Response
from metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    ACTIVE_REQUESTS
)

app = FastAPI()

@app.middleware("http")
async def metrics_middleware(request, call_next):
    method = request.method
    endpoint = request.url.path

    # A request has started
    ACTIVE_REQUESTS.inc()

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    # Count this request
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=str(response.status_code)
    ).inc()

    # Record how long it took
    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)

    # Request finished
    ACTIVE_REQUESTS.dec()

    return response

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

    end_time = time.time() + 10      # Burn CPU for 10 seconds

    x = 0

    while time.time() < end_time:
        x += 1

    return {
        "status": "CPU work completed",
        "hostname": socket.gethostname()
    }
# -----------------------------
# Memory Leak (OOMKilled Test)
# -----------------------------
memory_store = []

@app.get("/memory")
def memory_test():
    for _ in range(400):   # Allocate ~400 MB
        memory_store.append("A" * 1024 * 1024)
        time.sleep(0.2)

    return {"status": "Memory allocated"}


from prometheus_client import generate_latest, CONTENT_TYPE_LATEST      
@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )




@app.get("/error")
def error():
    raise HTTPException(
        status_code=500,
        detail="Internal Server Error"
    )