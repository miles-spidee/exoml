# Prediction endpoints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os
import joblib
import numpy as np
from .utils import validate_features

router = APIRouter()

# Initialize model artifacts
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
MODEL_PATH = os.path.join(MODEL_DIR, "exoplanet_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "exoplanet_scaler.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "model_features.pkl")

# Load model artifacts
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    print("✅ Model, scaler, and feature list loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model artifacts: {e}")
    model = None
    scaler = None
    feature_names = None

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
        # Check if model is loaded
        if model is None or scaler is None:
            raise HTTPException(status_code=500, detail="Model not loaded properly")
        
        # Validate input features
        if not validate_features(request.features):
            raise HTTPException(status_code=400, detail="Invalid features provided")
        
        # Check feature count
        if len(request.features) != len(feature_names):
            raise HTTPException(
                status_code=400, 
                detail=f"Expected {len(feature_names)} features, got {len(request.features)}"
            )
        
        # Prepare features for prediction
        features_array = np.array(request.features).reshape(1, -1)
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Calculate confidence and probability
        confidence = float(max(probabilities))
        exoplanet_probability = float(probabilities[1])
        
        # Interpret result
        interpretation = "Exoplanet detected!" if prediction == 1 else "No exoplanet detected"
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=exoplanet_probability,
            confidence=confidence,
            interpretation=interpretation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/model/info")
async def get_model_info():
    """Get information about the loaded model."""
    return {
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "feature_names": feature_names,
        "model_type": type(model).__name__ if model else None,
        "expected_features": len(feature_names) if feature_names else 0
    }