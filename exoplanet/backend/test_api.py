# test_api.py - Test the exoplanet prediction API

import requests
import json

# Test data from our previous analysis
test_cases = [
    {
        "name": "K00752.01 - CONFIRMED Exoplanet",
        "features": [9.48803557, 2.9575, 615.8, 2.26, 793.0, 93.59, 5455.0],
        "expected": "Exoplanet",
        "actual_label": "CONFIRMED"
    },
    {
        "name": "K00752.02 - CONFIRMED Exoplanet", 
        "features": [54.4183827, 4.507, 874.8, 2.83, 443.0, 9.11, 5455.0],
        "expected": "Exoplanet",
        "actual_label": "CONFIRMED"
    },
    {
        "name": "K00754.01 - FALSE POSITIVE",
        "features": [1.736952453, 2.40641, 8079.2, 33.46, 1395.0, 891.96, 5805.0],
        "expected": "Not Exoplanet", 
        "actual_label": "FALSE POSITIVE"
    },
    {
        "name": "K00114.01 - FALSE POSITIVE",
        "features": [7.36178958, 5.022, 233.7, 39.21, 1342.0, 767.22, 6227.0],
        "expected": "Not Exoplanet",
        "actual_label": "FALSE POSITIVE"
    }
]

# Feature names for reference
feature_names = ['koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq', 'koi_insol', 'koi_steff']

def test_api_endpoint(base_url="http://127.0.0.1:8000"):
    """Test the API with our sample data"""
    
    print("="*70)
    print("TESTING EXOPLANET PREDICTION API")
    print("="*70)
    
    # Test health endpoint first
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
        else:
            print(f"❌ API Health Check: FAILED (Status: {response.status_code})")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ API Health Check: FAILED (Error: {e})")
        print("Make sure the API server is running on http://127.0.0.1:8000")
        return
    
    print(f"\nTesting {len(test_cases)} samples through API...")
    print("-" * 70)
    
    correct_predictions = 0
    total_predictions = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['name']}")
        print(f"   Actual Label: {test_case['actual_label']}")
        print(f"   Expected: {test_case['expected']}")
        
        # Prepare API request
        payload = {
            "features": test_case['features'],
            "feature_names": feature_names
        }
        
        try:
            response = requests.post(f"{base_url}/predict", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Interpret prediction
                predicted_label = "Exoplanet" if result['prediction'] == 1 else "Not Exoplanet"
                is_correct = predicted_label == test_case['expected']
                
                if is_correct:
                    correct_predictions += 1
                total_predictions += 1
                
                print(f"   API Response: {predicted_label}")
                print(f"   Confidence: {result['confidence']:.4f}")
                print(f"   Exoplanet Probability: {result['probability']:.4f}")
                print(f"   Result: {'✅ CORRECT' if is_correct else '❌ INCORRECT'}")
                
            else:
                print(f"   ❌ API Error: Status {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request Failed: {e}")
    
    print("\n" + "="*70)
    print("API TEST RESULTS")
    print("="*70)
    print(f"Total API Tests: {total_predictions}")
    print(f"Correct Predictions: {correct_predictions}")
    if total_predictions > 0:
        print(f"API Test Accuracy: {correct_predictions/total_predictions:.2%}")
        
        if correct_predictions == total_predictions:
            print("🎉 ALL API TESTS PASSED! The API is working correctly.")
        else:
            print(f"⚠️  {total_predictions - correct_predictions} API test(s) failed.")
    else:
        print("❌ No successful API tests completed.")

if __name__ == "__main__":
    test_api_endpoint()