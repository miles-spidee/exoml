# run_clean_predictions.py - Clean production-ready prediction script

import json
import joblib
import numpy as np
from datetime import datetime
import os

def load_model_artifacts():
    """Load the trained model, scaler, and feature names"""
    try:
        model = joblib.load('./backend/models/exoplanet_model.pkl')
        scaler = joblib.load('./backend/models/exoplanet_scaler.pkl')
        feature_names = joblib.load('./backend/models/model_features.pkl')
        return model, scaler, feature_names
    except Exception as e:
        raise Exception(f"Error loading model artifacts: {e}")

def make_prediction(model, scaler, features_dict, feature_names):
    """Make a prediction for a single sample"""
    # Extract features in the correct order
    features = [features_dict[name] for name in feature_names]
    
    # Convert to numpy array and reshape
    features_array = np.array(features).reshape(1, -1)
    
    # Scale the features
    features_scaled = scaler.transform(features_array)
    
    # Make prediction
    prediction = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]
    
    return {
        "prediction": int(prediction),
        "prediction_label": "Exoplanet" if prediction == 1 else "Not Exoplanet",
        "confidence": round(float(max(probabilities)), 4),
        "exoplanet_probability": round(float(probabilities[1]), 4)
    }

def main():
    print("🚀 Running Exoplanet Predictions...")
    
    # Load model artifacts
    try:
        model, scaler, feature_names = load_model_artifacts()
        print(f"✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Read input JSON
    try:
        with open('input.json', 'r') as f:
            input_data = json.load(f)
        print(f"✅ Processing {len(input_data['predictions'])} samples...")
    except Exception as e:
        print(f"❌ Failed to read input.json: {e}")
        return
    
    # Process each sample
    results = []
    
    for sample in input_data['predictions']:
        try:
            # Extract run_id and features
            run_id = sample['run_id']
            
            # Create features dictionary (excluding run_id)
            features_dict = {k: v for k, v in sample.items() if k != 'run_id'}
            
            # Make prediction
            prediction_result = make_prediction(model, scaler, features_dict, feature_names)
            
            # Prepare clean result
            result = {
                "run_id": run_id,
                "parameters": features_dict,
                "result": prediction_result,
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(result)
            print(f"   {run_id}: {prediction_result['prediction_label']} (confidence: {prediction_result['confidence']})")
            
        except Exception as e:
            print(f"   ❌ Error processing {sample.get('run_id', 'unknown')}: {e}")
            continue
    
    # Prepare clean output data
    output_data = {
        "prediction_batch": {
            "timestamp": datetime.now().isoformat(),
            "total_predictions": len(results),
            "model_version": "exoplanet_v1.0"
        },
        "results": results
    }
    
    # Write clean output JSON
    try:
        with open('predictions_log.json', 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"✅ Results saved to predictions_log.json")
    except Exception as e:
        print(f"❌ Failed to write output: {e}")
        return
    
    print(f"🎯 Completed {len(results)} predictions successfully!")

if __name__ == "__main__":
    main()