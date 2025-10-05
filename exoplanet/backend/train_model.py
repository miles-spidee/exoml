# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# --- Configuration ---
# Define file paths based on your project structure
DATA_PATH = "../data/kepler.csv"  # Assuming data folder is at project root
MODEL_OUTPUT_DIR = "./models"  # Models folder in current backend directory
MODEL_NAME = "exoplanet_model.pkl"
SCALER_NAME = "exoplanet_scaler.pkl"
FEATURES_NAME = "model_features.pkl"

# --- 1. Load the Data
# 
#  ---
print(f"Loading data from {DATA_PATH}...")
try:
    # Kepler data often has commented lines at the top; we skip them
    with open(DATA_PATH, 'r') as f:
        first_line = 0
        for line in f:
            if not line.startswith('#'):
                break
            first_line += 1
    
    df = pd.read_csv(DATA_PATH, skiprows=first_line)
    print("Data loaded successfully!")
except FileNotFoundError:
    print(f"❌ Error: '{DATA_PATH}' not found. Make sure your data is in the correct folder.")
    exit()

# --- 2. Clean and Prepare Data ---
print("Cleaning and preparing data...")
# For this model, we'll classify objects as either an exoplanet or not.
# 'CONFIRMED' and 'CANDIDATE' are positive (1), 'FALSE POSITIVE' is negative (0).
df['is_exoplanet'] = df['koi_disposition'].apply(lambda x: 1 if x in ['CONFIRMED', 'CANDIDATE'] else 0)

# These are the features we will use to train the model.
# They are chosen because they are numerical and highly relevant.
features_to_use = [
    'koi_period', 'koi_duration', 'koi_depth', 'koi_prad',
    'koi_teq', 'koi_insol', 'koi_steff'
]
target = 'is_exoplanet'

# Drop rows with missing values in our selected columns for simplicity
model_df = df[features_to_use + [target]].dropna()
print(f"Data cleaned. Using {len(model_df)} rows for the model.")

# --- 3. Define Features (X) and Target (y) ---
X = model_df[features_to_use]
y = model_df[target]

# --- 4. Split and Scale Data ---
print("Splitting and scaling data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# Scaling is critical for MLP models
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test) # Use the same scaler fitted on the training data

# --- 5. Train the MLP Model ---
print("Training the MLP model... (This might take a moment)")
model = MLPClassifier(
    hidden_layer_sizes=(100, 50), # 2 hidden layers
    max_iter=500,
    activation='relu',
    solver='adam',
    random_state=42,
    verbose=False # Set to True to see training progress
)
model.fit(X_train_scaled, y_train)
print("Model training complete!")

# --- 6. Evaluate the Model ---
print("\n--- Model Evaluation ---")
predictions = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy on Test Data: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=['Not an Exoplanet', 'Exoplanet Candidate']))

# --- 7. Save the Model, Scaler, and Features ---
print(f"Saving artifacts to {MODEL_OUTPUT_DIR}...")
# Create the directory if it doesn't exist
os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_OUTPUT_DIR, MODEL_NAME))
joblib.dump(scaler, os.path.join(MODEL_OUTPUT_DIR, SCALER_NAME))
joblib.dump(features_to_use, os.path.join(MODEL_OUTPUT_DIR, FEATURES_NAME))

print("\n✅ All done! Your model, scaler, and feature list are saved and ready for the backend.")
