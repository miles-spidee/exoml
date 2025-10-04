# backend/app/model.py

import joblib
from pathlib import Path

# --- LOAD THE MODEL AND SCALER ---

# Build the path to the models directory
# This makes the path independent of where you run the script from
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
MODEL_DIR = BASE_DIR / "models"

try:
    # Load the trained model, scaler, and feature list
    model = joblib.load(MODEL_DIR / "exoplanet_model.pkl")
    scaler = joblib.load(MODEL_DIR / "exoplanet_scaler.pkl")
    model_features = joblib.load(MODEL_DIR / "model_features.pkl")
    print("✅ Model, scaler, and feature list loaded successfully!")

except FileNotFoundError as e:
    print(f"❌ Error loading model files: {e}")
    print(f"Ensure model files exist in the '{MODEL_DIR}' directory.")
    model = None
    scaler = None
    model_features = None