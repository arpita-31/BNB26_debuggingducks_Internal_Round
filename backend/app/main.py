"""
Main FastAPI Application Entrypoint for ReLearn
Configures CORS, registers modular API routers, initializes database,
and serves the cognitive learning pipeline.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.db import init_db
from app.database.seed import seed_database
from app.diagnosis.engine import diagnosis_engine
from app.api.routes_auth import router as auth_router
from app.api.routes_teacher import router as teacher_router
from app.api.routes_n8n import router as n8n_router
from app.api.routes_diagnosis import router as diagnosis_router
from app.api.routes_intervention import router as intervention_router
from app.api.routes_reassessment import router as reassessment_router
from app.api.routes_learner import router as learner_router
from app.api.routes_questions import router as questions_router
from app.api.routes_model import router as model_router
from app.api.routes_demo import router as demo_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence
    print("[ReLearn] Initializing database and models...")
    init_db()
    seed_database()
    # Ensure ML model is loaded
    diagnosis_engine._ensure_model_loaded()
    print("[ReLearn] Backend initialized successfully.")
    yield
    print("[ReLearn] Shutting down.")

app = FastAPI(
    title="ReLearn API",
    description="Adaptive Multimodal Learning Environment with Causal Cognitive Diagnosis",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local Vite development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router)
app.include_router(teacher_router)
app.include_router(n8n_router)
app.include_router(diagnosis_router)
app.include_router(intervention_router)
app.include_router(reassessment_router)
app.include_router(learner_router)
app.include_router(questions_router)
app.include_router(model_router)
app.include_router(demo_router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ReLearn Backend",
        "version": "1.0.0",
        "ml_model_status": "loaded" if diagnosis_engine.model is not None else "initializing"
    }

# Mount Static Web Assets (must be after all API routes)
from fastapi.staticfiles import StaticFiles
from pathlib import Path
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
