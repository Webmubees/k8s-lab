from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/")
def home():
    return {
        "service" : "Product Service",
        "hostname" : socket.gethostname() ,
        "Products" : [
            {
                "id" : 1,
                "name" : "Laptop"
            },
            {
                "id" : 2,
                "name" : "Keyboard"
            },
            {
                "id" : 3,
                "name" : "Mouse"
            }
        ]
    }

@app.get("/health")
def health():
    return {
        "startus" : "healty"
    }