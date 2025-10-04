# run_predictions.py - Read input.json, make predictions, write to output JSON

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
        "confidence": float(max(probabilities)),
        "exoplanet_probability": float(probabilities[1]),
        "not_exoplanet_probability": float(probabilities[0])
    }

def main():
    print("🚀 Starting Exoplanet Prediction Pipeline...")
    print("=" * 60)
    
    # Load model artifacts
    print("📦 Loading trained model...")
    try:
        model, scaler, feature_names = load_model_artifacts()
        print(f"✅ Model loaded successfully!")
        print(f"   Features used: {feature_names}")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Read input JSON
    print("\n📁 Reading input.json...")
    try:
        with open('input.json', 'r') as f:
            input_data = json.load(f)
        print(f"✅ Input data loaded with {len(input_data['test_samples'])} samples")
    except Exception as e:
        print(f"❌ Failed to read input.json: {e}")
        return
    
    # Process each sample
    print("\n🔮 Making predictions...")
    results = []
    correct_predictions = 0
    total_predictions = 0
    
    for i, sample in enumerate(input_data['test_samples'], 1):
        print(f"\n   Sample {i}: {sample['name']}")
        
        try:
            # Make prediction
            prediction_result = make_prediction(
                model, scaler, sample['features'], feature_names
            )
            
            # Check if prediction is correct
            is_correct = prediction_result['prediction'] == sample['expected_prediction']
            if is_correct:
                correct_predictions += 1
            total_predictions += 1
            
            # Prepare result
            result = {
                "sample_id": i,
                "name": sample['name'],
                "expected_label": sample['expected_label'],
                "expected_prediction": sample['expected_prediction'],
                "input_features": sample['features'],
                "prediction_result": prediction_result,
                "is_correct": is_correct,
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(result)
            
            # Display result
            status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
            print(f"      Expected: {sample['expected_label']}")
            print(f"      Predicted: {prediction_result['prediction_label']}")
            print(f"      Confidence: {prediction_result['confidence']:.4f}")
            print(f"      Status: {status}")
            
        except Exception as e:
            print(f"      ❌ Error making prediction: {e}")
            continue
    
    # Calculate accuracy
    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    
    # Prepare output data
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "model_info": {
            "features_used": feature_names,
            "total_samples": total_predictions,
            "correct_predictions": correct_predictions,
            "accuracy": accuracy
        },
        "summary": {
            "total_tests": total_predictions,
            "correct": correct_predictions,
            "incorrect": total_predictions - correct_predictions,
            "accuracy_percentage": f"{accuracy:.2%}"
        },
        "detailed_results": results
    }
    
    # Write output JSON
    print(f"\n💾 Writing results to predictions_log.json...")
    try:
        with open('predictions_log.json', 'w') as f:
            json.dump(output_data, f, indent=2)
        print("✅ Results saved successfully!")
    except Exception as e:
        print(f"❌ Failed to write output: {e}")
        return
    
    # Display final summary
    print("\n" + "=" * 60)
    print("🎯 FINAL RESULTS SUMMARY")
    print("=" * 60)
    print(f"📊 Total Samples Tested: {total_predictions}")
    print(f"✅ Correct Predictions: {correct_predictions}")
    print(f"❌ Incorrect Predictions: {total_predictions - correct_predictions}")
    print(f"🎯 Overall Accuracy: {accuracy:.2%}")
    
    if accuracy == 1.0:
        print("🎉 PERFECT SCORE! All predictions were correct!")
    elif accuracy >= 0.75:
        print("👍 GOOD PERFORMANCE! Model is working well.")
    elif accuracy >= 0.5:
        print("⚠️  MODERATE PERFORMANCE. Model may need improvements.")
    else:
        print("🔴 POOR PERFORMANCE. Model needs significant improvements.")
    
    print(f"\n📄 Detailed results saved in: predictions_log.json")
    print("🚀 Prediction pipeline completed!")

if __name__ == "__main__":
    main()