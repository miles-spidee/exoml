# backend/app/predict.py

import pandas as pd
from .model import model, scaler # Import loaded model and scaler

def make_prediction(input_df: pd.DataFrame) -> str:
    """
    Takes preprocessed data, scales it, and returns a prediction.
    """
    if model is None or scaler is None:
        raise RuntimeError("Model or scaler not loaded.")

    # Scale the input data using the loaded scaler
    input_scaled = scaler.transform(input_df)
    
    # Make a prediction (it returns an array, e.g., [0] or [1])
    prediction_raw = model.predict(input_scaled)
    
    # Get the first element and convert it to a human-readable label
    prediction_result = int(prediction_raw[0])
    final_prediction = "Exoplanet Candidate" if prediction_result == 1 else "Not an Exoplanet"
    
    return final_prediction