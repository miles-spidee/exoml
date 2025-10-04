# test_model.py - Test the trained exoplanet model with specific examples

import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load the trained model, scaler, and features
print("Loading trained model artifacts...")
model = joblib.load('./models/exoplanet_model.pkl')
scaler = joblib.load('./models/exoplanet_scaler.pkl')
features_to_use = joblib.load('./models/model_features.pkl')

print(f"Features used by model: {features_to_use}")

# Load the dataset to extract test samples
print("\nLoading Kepler dataset...")
with open('../data/kepler.csv', 'r') as f:
    first_line = 0
    for line in f:
        if not line.startswith('#'):
            break
        first_line += 1

df = pd.read_csv('../data/kepler.csv', skiprows=first_line)

# Create target variable
df['is_exoplanet'] = df['koi_disposition'].apply(lambda x: 1 if x in ['CONFIRMED', 'CANDIDATE'] else 0)

# Clean data - remove rows with missing values in our features
clean_df = df[features_to_use + ['koi_disposition', 'is_exoplanet', 'kepoi_name']].dropna()

print(f"\nDataset info after cleaning:")
print(f"Total samples: {len(clean_df)}")
print(f"Exoplanet candidates (CONFIRMED/CANDIDATE): {len(clean_df[clean_df['is_exoplanet'] == 1])}")
print(f"False positives: {len(clean_df[clean_df['is_exoplanet'] == 0])}")

# Extract test samples
print("\n" + "="*60)
print("EXTRACTING TEST SAMPLES")
print("="*60)

# Get 2 confirmed exoplanet candidates
exoplanet_samples = clean_df[clean_df['koi_disposition'] == 'CONFIRMED'].head(2)
print(f"\n🌟 EXOPLANET CANDIDATES (Expected: Positive)")
for idx, (_, row) in enumerate(exoplanet_samples.iterrows(), 1):
    print(f"\nCandidate {idx}: {row['kepoi_name']} - {row['koi_disposition']}")
    feature_values = [row[feature] for feature in features_to_use]
    print(f"Features: {dict(zip(features_to_use, feature_values))}")

# Get 2 false positives
false_positive_samples = clean_df[clean_df['koi_disposition'] == 'FALSE POSITIVE'].head(2)
print(f"\n❌ FALSE POSITIVES (Expected: Negative)")
for idx, (_, row) in enumerate(false_positive_samples.iterrows(), 1):
    print(f"\nFalse Positive {idx}: {row['kepoi_name']} - {row['koi_disposition']}")
    feature_values = [row[feature] for feature in features_to_use]
    print(f"Features: {dict(zip(features_to_use, feature_values))}")

# Combine all test samples
all_test_samples = pd.concat([exoplanet_samples, false_positive_samples])

print("\n" + "="*60)
print("MAKING PREDICTIONS")
print("="*60)

# Make predictions
correct_predictions = 0
total_predictions = 0

for idx, (_, row) in enumerate(all_test_samples.iterrows(), 1):
    # Extract features
    features = np.array([row[feature] for feature in features_to_use]).reshape(1, -1)
    
    # Scale features using the same scaler from training
    features_scaled = scaler.transform(features)
    
    # Make prediction
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]
    
    # Determine expected result
    expected = row['is_exoplanet']
    actual_label = row['koi_disposition']
    sample_name = row['kepoi_name']
    
    # Check if prediction is correct
    is_correct = prediction == expected
    if is_correct:
        correct_predictions += 1
    total_predictions += 1
    
    # Display results
    print(f"\n📊 Test Sample {idx}: {sample_name}")
    print(f"   Actual Label: {actual_label}")
    print(f"   Expected: {'Exoplanet' if expected == 1 else 'Not Exoplanet'} ({expected})")
    print(f"   Predicted: {'Exoplanet' if prediction == 1 else 'Not Exoplanet'} ({prediction})")
    print(f"   Confidence: {max(probability):.4f}")
    print(f"   Exoplanet Probability: {probability[1]:.4f}")
    print(f"   Result: {'✅ CORRECT' if is_correct else '❌ INCORRECT'}")

print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)
print(f"Total Test Samples: {total_predictions}")
print(f"Correct Predictions: {correct_predictions}")
print(f"Test Accuracy: {correct_predictions/total_predictions:.2%}")

if correct_predictions == total_predictions:
    print("🎉 ALL PREDICTIONS CORRECT! Model is working perfectly on test samples.")
else:
    print(f"⚠️  {total_predictions - correct_predictions} prediction(s) incorrect. Model may need tuning.")

print("\n" + "="*60)
print("DETAILED FEATURE ANALYSIS")
print("="*60)

# Show feature importance analysis
print(f"\nFeature ranges in dataset:")
for feature in features_to_use:
    feature_data = clean_df[feature]
    print(f"{feature}:")
    print(f"  Min: {feature_data.min():.4f}")
    print(f"  Max: {feature_data.max():.4f}")
    print(f"  Mean: {feature_data.mean():.4f}")
    print(f"  Std: {feature_data.std():.4f}")