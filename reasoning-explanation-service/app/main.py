from fastapi import FastAPI
from .api.routes import router


app = FastAPI(
    title="Reasoning & Explanation Service",
    version="1.0.0"
)

app.include_router(router)
