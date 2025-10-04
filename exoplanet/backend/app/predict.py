from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import numpy as np
from datetime import datetime

from .utils import load_model_artifacts, validate_features, prepare_features_for_prediction

router = APIRouter()

# Global variables to store loaded model artifacts
model = None
scaler = None
feature_names = None

class PredictionRequest(BaseModel):
    koi_period: float
    koi_duration: float
    koi_depth: float
    koi_prad: float
    koi_teq: float
    koi_insol: float
    koi_steff: float

class PredictionResponse(BaseModel):
    prediction: int
    prediction_label: str
    confidence: float
    exoplanet_probability: float
    not_exoplanet_probability: float
    timestamp: str

def load_model():
    """Load model artifacts on startup"""
    global model, scaler, feature_names
    try:
        model, scaler, feature_names = load_model_artifacts()
        return True
    except Exception as e:
        print(f"Failed to load model: {e}")
        return False

@router.on_event("startup")
async def startup_event():
    """Load model when the API starts"""
    success = load_model()
    if not success:
        print("Warning: Model failed to load on startup")

@router.post("/predict", response_model=PredictionResponse)
async def predict_exoplanet(request: PredictionRequest):
    """
    Predict whether the given parameters indicate an exoplanet
    """
    global model, scaler, feature_names
    
    # Ensure model is loaded
    if model is None or scaler is None or feature_names is None:
        success = load_model()
        if not success:
            raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert request to dictionary
        features = request.dict()
        
        # Validate features
        validation = validate_features(features)
        if not validation["is_valid"]:
            raise HTTPException(status_code=400, detail=f"Invalid input: {validation['errors']}")
        
        # Prepare features for prediction
        features_array = prepare_features_for_prediction(features, feature_names)
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Prepare response
        response = PredictionResponse(
            prediction=int(prediction),
            prediction_label="Exoplanet" if prediction == 1 else "Not Exoplanet",
            confidence=float(max(probabilities)),
            exoplanet_probability=float(probabilities[1]),
            not_exoplanet_probability=float(probabilities[0]),
            timestamp=datetime.now().isoformat()
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/model/info")
async def get_model_info():
    """Get information about the loaded model"""
    global model, scaler, feature_names
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "features": feature_names,
        "feature_count": len(feature_names),
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    }