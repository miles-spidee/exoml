import joblib
import numpy as np
from typing import Dict, List, Any
import os

def load_model_artifacts():
    """Load the trained model, scaler, and feature names"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), '../models/exoplanet_model.pkl')
        scaler_path = os.path.join(os.path.dirname(__file__), '../models/exoplanet_scaler.pkl')
        features_path = os.path.join(os.path.dirname(__file__), '../models/model_features.pkl')
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_names = joblib.load(features_path)
        
        return model, scaler, feature_names
    except Exception as e:
        raise Exception(f"Error loading model artifacts: {e}")

def validate_features(features: Dict[str, float]) -> Dict[str, Any]:
    """
    Validate input features for exoplanet prediction
    
    Args:
        features: Dictionary of feature names and values
        
    Returns:
        Dictionary with validation results
    """
    required_features = [
        'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 
        'koi_teq', 'koi_insol', 'koi_steff'
    ]
    
    validation_result = {
        "is_valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check for missing features
    missing_features = [f for f in required_features if f not in features]
    if missing_features:
        validation_result["is_valid"] = False
        validation_result["errors"].append(f"Missing required features: {missing_features}")
    
    # Check for valid numeric values
    for feature_name in required_features:
        if feature_name in features:
            value = features[feature_name]
            if not isinstance(value, (int, float)):
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"{feature_name} must be a number")
            elif value < 0:
                validation_result["warnings"].append(f"{feature_name} is negative, which may be unusual")
    
    # Feature-specific validations
    if 'koi_period' in features and features['koi_period'] > 10000:
        validation_result["warnings"].append("Orbital period > 10,000 days is very long")
    
    if 'koi_duration' in features and features['koi_duration'] > 100:
        validation_result["warnings"].append("Transit duration > 100 hours is very long")
    
    if 'koi_steff' in features:
        temp = features['koi_steff']
        if temp < 2000 or temp > 10000:
            validation_result["warnings"].append("Stellar temperature outside typical range (2000-10000K)")
    
    return validation_result

def prepare_features_for_prediction(features: Dict[str, float], feature_names: List[str]) -> np.ndarray:
    """
    Prepare features for model prediction
    
    Args:
        features: Dictionary of feature values
        feature_names: List of feature names in correct order
        
    Returns:
        Numpy array of features ready for prediction
    """
    # Extract features in the correct order
    feature_values = [features[name] for name in feature_names]
    
    # Convert to numpy array and reshape for single prediction
    return np.array(feature_values).reshape(1, -1)