from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, patients, appointments, doctors, admin
from database import init_db
import sys

app = FastAPI(
    title="Hospital Management System with AI Receptionist",
    version="2.0.0",
    description="Complete hospital management platform with AI-powered patient intake"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://hospital-ai-agent.onrender.com", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
        print("[SUCCESS] Database initialized")
    except Exception as e:
        print(f"[WARNING] Database initialization failed: {e}")
        # Don't crash on startup - allow app to run without DB for now

@app.get("/")
async def root():
    return {
        "message": "Hospital Management System API",
        "version": "2.0.0",
        "documentation": "/docs"
    }

@app.get("/health")
async def health():
    """Health check endpoint for Render"""
    return {"status": "ok", "service": "hospital-ai-backend"}

# Include routers
try:
    app.include_router(chat.router, prefix="/api")
    app.include_router(patients.router, prefix="/api")
    app.include_router(appointments.appointments_router, prefix="/api")
    app.include_router(appointments.departments_router, prefix="/api")
    app.include_router(doctors.router, prefix="/api")
    app.include_router(admin.router, prefix="/api")
    app.include_router(admin.feedback_router, prefix="/api")
    print("[SUCCESS] All routers loaded")
except Exception as e:
    print(f"[ERROR] Failed to load routers: {e}", file=sys.stderr)
    sys.exit(1)