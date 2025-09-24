from fastapi import FastAPI
from fastapi.routing import APIRoute
from main import app

def list_routes():
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"{route.path} - {route.methods} - {route.name}")

if __name__ == "__main__":
    list_routes()
