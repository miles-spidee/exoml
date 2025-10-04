# backend/app/utils.py

from pydantic import BaseModel
import pandas as pd
from typing import List

# --- DATA VALIDATION MODEL ---

# Use Pydantic to define the structure of the input data
# This provides automatic data validation and clear error messages.
# The feature names here MUST match the ones your model was trained on.
class ExoplanetData(BaseModel):
    koi_period: float
    koi_duration: float
    koi_depth: float
    koi_prad: float
    koi_teq: float
    koi_insol: float
    koi_steff: float


# --- DATA PREPROCESSING FUNCTION ---

def preprocess_input(data: ExoplanetData, feature_order: List[str]) -> pd.DataFrame:
    """
    Converts the Pydantic model into a Pandas DataFrame with the
    correct column order for the model.
    """
    # Convert the Pydantic model to a dictionary
    input_dict = data.dict()
    
    # Create a DataFrame from the dictionary, ensuring the correct feature order
    input_df = pd.DataFrame([input_dict], columns=feature_order)
    
    return input_df