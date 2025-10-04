# backend/app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .utils import ExoplanetData, preprocess_input
from .predict import make_prediction
from .model import model_features

# Initialize the FastAPI app
app = FastAPI(title="Exoplanet Prediction API")

# --- MIDDLEWARE ---
# Setup CORS (Cross-Origin Resource Sharing) to allow your React frontend
# to communicate with this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- API ENDPOINTS ---

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to check if the API is running."""
    return {"message": "Welcome to the Exoplanet Prediction API!"}


@app.post("/predict", tags=["Prediction"])
def predict(data: ExoplanetData):
    """
    Receives exoplanet data and returns a prediction.
    The `data: ExoplanetData` part automatically validates the incoming JSON.
    """
    if not model_features:
        raise HTTPException(status_code=500, detail="Model features not loaded.")

    try:
        # 1. Preprocess the input data
        input_df = preprocess_input(data, model_features)
        
        # 2. Make a prediction
        prediction = make_prediction(input_df)
        
        # 3. Return the result
        return {"prediction": prediction}
        
    except Exception as e:
        # Handle any errors that occur during the process
        raise HTTPException(status_code=500, detail=str(e))