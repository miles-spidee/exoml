# Machine learning model utilities
import pickle
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ExoplanetModel:
    def __init__(self, model_path: str):
        """Initialize the exoplanet detection model."""
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model from pickle file."""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            logger.info(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def preprocess_data(self, features: List[float]) -> np.ndarray:
        """Preprocess input features for prediction."""
        return np.array(features).reshape(1, -1)
    
    def predict(self, features: List[float]) -> Dict[str, Any]:
        """Make prediction on input features."""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            processed_features = self.preprocess_data(features)
            prediction = self.model.predict(processed_features)
            probability = self.model.predict_proba(processed_features)
            
            return {
                "prediction": int(prediction[0]),
                "probability": float(probability[0][1]),  # Probability of exoplanet
                "confidence": float(max(probability[0]))
            }
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise