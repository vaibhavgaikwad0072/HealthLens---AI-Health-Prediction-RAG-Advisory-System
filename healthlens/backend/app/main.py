from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

from .api.endpoints import router as api_router
from .database.connection import connect_db

description = """
HealthLens API: AI-powered healthcare system.
Includes intelligent endpoints for risk predictions, smartwatch data integration via Google Fit, and a FAISS-RAG based Health Advisor Chatbot.
"""

app = FastAPI(
    title="HealthLens API",
    description=description,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def startup_event():
    connect_db()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "HealthLens API is running"}
