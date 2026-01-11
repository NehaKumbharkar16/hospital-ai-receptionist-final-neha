from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat
from database import init_db

app = FastAPI(title="Hospital AI Receptionist", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://hospital-ai-agent.onrender.com", "*"],  # Allow local dev, production, and all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Hospital AI Receptionist API"}

app.include_router(chat.router, prefix="/api")