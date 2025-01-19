from fastapi import FastAPI
from .routers import group, worker

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

@app.get('/')
def root():
    return {'message': 'Welcome! Some magic happened here.'}

app.include_router(group.router)
app.include_router(worker.router)