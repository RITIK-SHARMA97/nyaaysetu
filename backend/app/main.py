from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import create_tables
from app.api import auth, judgments, actions, dashboard, officers

app = FastAPI(
    title="NyaaySetu API",
    description="AI-powered court compliance management for Karnataka Government",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(judgments.router)
app.include_router(actions.router)
app.include_router(dashboard.router)
app.include_router(officers.router)

# Serve uploaded PDFs statically for frontend PDF viewer
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.on_event("startup")
def startup():
    create_tables()
    print("✅ NyaaySetu API started. Docs: http://localhost:8000/docs")

@app.get("/")
def root():
    return {
        "app": "NyaaySetu",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "description": "Court compliance management for Karnataka Government"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
