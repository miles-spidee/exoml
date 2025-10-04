# Utility functions
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def validate_features(features: List[float]) -> bool:
    """Validate input features for exoplanet prediction."""
    if not features:
        return False
    
    if len(features) == 0:
        return False
    
    # Check for NaN or infinite values
    try:
        features_array = np.array(features)
        if np.any(np.isnan(features_array)) or np.any(np.isinf(features_array)):
            return False
    except Exception as e:
        logger.error(f"Error validating features: {e}")
        return False
    
    return True

def normalize_features(features: List[float]) -> List[float]:
    """Normalize features to standard scale."""
    features_array = np.array(features)
    # Simple min-max normalization
    normalized = (features_array - np.min(features_array)) / (np.max(features_array) - np.min(features_array))
    return normalized.tolist()

def calculate_feature_importance(features: List[float], feature_names: List[str] = None) -> Dict[str, float]:
    """Calculate relative importance of features."""
    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(len(features))]
    
    # Simple importance based on absolute values
    total = sum(abs(f) for f in features)
    if total == 0:
        return {name: 0.0 for name in feature_names}
    
    importance = {name: abs(value) / total for name, value in zip(feature_names, features)}
    return importance

def log_prediction(features: List[float], prediction: Dict[str, Any]):
    """Log prediction for monitoring purposes."""
    logger.info(f"Prediction made: {prediction} for features: {features[:3]}...")  # Log first 3 features for privacy