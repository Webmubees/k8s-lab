from fastapi import FastAPI
import socket
import requests

app = FastAPI()

@app.get("/")
def home():
    return {
        "service": "User Service",
        "hostname": socket.gethostname()
    }

@app.get("/products")
def products():
    return  requests.get("http://product-service").json()
   

  
@app.get("/info")
def info():
    product = requests.get("http://product-service").json()
    general = requests.get("http://general-service").json()

    return {
        "users": {
            "name": "Mubees",
            "role": "Backend Engineer"
        },
        "products": product,
        "general" : general
    }
