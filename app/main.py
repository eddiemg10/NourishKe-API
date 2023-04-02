from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.v1 import router as v1_router

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, version="0.0.1")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
app.include_router(v1_router, prefix="/api")

@app.get("/")
def root():
    return {"Message": "Hello There"}
