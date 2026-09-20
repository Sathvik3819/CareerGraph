import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.stream import router as stream_router
from app.routes.resume import router as resume_router
from app.database import Base, engine
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]

app = FastAPI(
    title="CareerGraph API",
    description="Agentic Job-Tailored Resume Generation Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "CareerGraph API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

app.include_router(
    resume_router
)

app.include_router(
    stream_router
)

app.include_router(
    auth_router
)