# Main FastAPI application entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .predict import router as predict_router

app = FastAPI(title="Exoplanet Detection API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include prediction routes
app.include_router(predict_router, prefix="", tags=["predictions"])

@app.get("/")
async def root():
    return {"message": "Exoplanet Detection API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}