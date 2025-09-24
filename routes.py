from fastapi import FastAPI
from fastapi.routing import APIRoute
from main import app

def list_routes():
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append({
                "path": route.path,
                "name": route.name,
                "methods": route.methods
            })
    return routes

@app.get("/routes")
async def get_routes():
    return list_routes()
