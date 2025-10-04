# Prediction endpoints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os
from .model import ExoplanetModel
from .utils import validate_features

router = APIRouter()

# Initialize model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/exoplanet_model.pkl")
model = ExoplanetModel(MODEL_PATH)

class PredictionRequest(BaseModel):
    features: List[float]
    feature_names: List[str] = None

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    confidence: float
    interpretation: str

@router.post("/predict", response_model=PredictionResponse)
async def predict_exoplanet(request: PredictionRequest):
    """Predict whether given features indicate an exoplanet."""
    try:
        # Validate input features
        if not validate_features(request.features):
            raise HTTPException(status_code=400, detail="Invalid features provided")
        
        # Make prediction
        result = model.predict(request.features)
        
        # Interpret result
        interpretation = "Exoplanet detected!" if result["prediction"] == 1 else "No exoplanet detected"
        
        return PredictionResponse(
            prediction=result["prediction"],
            probability=result["probability"],
            confidence=result["confidence"],
            interpretation=interpretation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/model/info")
async def get_model_info():
    """Get information about the loaded model."""
    return {
        "model_path": MODEL_PATH,
        "model_loaded": model.model is not None,
        "model_type": type(model.model).__name__ if model.model else None
    }