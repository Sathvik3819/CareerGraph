from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.stream import router as stream_router
from app.routes.resume import router as resume_router
from app.database import Base, engine
from app.models import ResumeRecord
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CareerGraph API",
    description="Agentic Job-Tailored Resume Generation Platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
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