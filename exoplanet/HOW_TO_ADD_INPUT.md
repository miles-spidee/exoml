# 🌟 How to Add Your Own Exoplanet Data - Complete Guide

## 📋 **Required Parameters for Each Prediction**

To make predictions with your own data, you need to provide these 7 features for each sample:

### **1. `koi_period` - Orbital Period (days)**
- **Description**: How long it takes the planet to orbit its star
- **Range**: 0.24 - 129,995 days (from dataset)
- **Example**: `10.5` (10.5 days)
- **Earth reference**: Earth = 365.25 days

### **2. `koi_duration` - Transit Duration (hours)**
- **Description**: How long the planet takes to cross in front of its star
- **Range**: 0.05 - 138.5 hours (from dataset)
- **Example**: `3.2` (3.2 hours)

### **3. `koi_depth` - Transit Depth (parts per million)**
- **Description**: How much the star's brightness dims during transit
- **Range**: 0 - 1,541,400 ppm (from dataset)
- **Example**: `500.0` (500 ppm = 0.05% dimming)

### **4. `koi_prad` - Planet Radius (Earth radii)**
- **Description**: Size of the planet compared to Earth
- **Range**: 0.08 - 200,346 Earth radii (from dataset)
- **Example**: `1.8` (1.8 times Earth's radius)
- **Earth reference**: Earth = 1.0

### **5. `koi_teq` - Equilibrium Temperature (Kelvin)**
- **Description**: Estimated temperature of the planet
- **Range**: 25 - 14,667 K (from dataset)
- **Example**: `700.0` (700 K = 427°C)
- **Earth reference**: Earth ≈ 255 K

### **6. `koi_insol` - Insolation Flux (Earth flux)**
- **Description**: Amount of stellar energy received compared to Earth
- **Range**: 0 - 10,947,554 Earth flux (from dataset)
- **Example**: `50.0` (50 times Earth's solar flux)
- **Earth reference**: Earth = 1.0

### **7. `koi_steff` - Stellar Effective Temperature (Kelvin)**
- **Description**: Temperature of the host star
- **Range**: 2,661 - 15,896 K (from dataset)
- **Example**: `5500.0` (5500 K, similar to our Sun)
- **Sun reference**: Sun ≈ 5778 K

## 📝 **JSON Structure Template**

```json
{
  "predictions": [
    {
      "run_id": "YOUR_UNIQUE_ID_1",
      "koi_period": YOUR_ORBITAL_PERIOD,
      "koi_duration": YOUR_TRANSIT_DURATION,
      "koi_depth": YOUR_TRANSIT_DEPTH,
      "koi_prad": YOUR_PLANET_RADIUS,
      "koi_teq": YOUR_PLANET_TEMPERATURE,
      "koi_insol": YOUR_INSOLATION_FLUX,
      "koi_steff": YOUR_STAR_TEMPERATURE
    }
  ]
}
```

## 🔬 **Example Input Scenarios**

### **Scenario 1: Hot Jupiter (likely exoplanet)**
```json
{
  "run_id": "HOT_JUPITER_001",
  "koi_period": 3.5,        // Short period (close to star)
  "koi_duration": 2.8,      // Moderate transit duration
  "koi_depth": 8000.0,      // Deep transit (large planet)
  "koi_prad": 11.2,         // Jupiter-sized (11x Earth radius)
  "koi_teq": 1200.0,        // Very hot (close to star)
  "koi_insol": 400.0,       // High stellar flux
  "koi_steff": 5800.0       // Sun-like star
}
```

### **Scenario 2: Earth-like Planet (likely exoplanet)**
```json
{
  "run_id": "EARTH_LIKE_001", 
  "koi_period": 365.0,      // Earth-like orbital period
  "koi_duration": 6.5,      // Longer transit duration
  "koi_depth": 84.0,        // Shallow transit (small planet)
  "koi_prad": 1.0,          // Earth-sized
  "koi_teq": 255.0,         // Earth-like temperature
  "koi_insol": 1.0,         // Earth-like flux
  "koi_steff": 5778.0       // Sun-like star
}
```

### **Scenario 3: False Positive (stellar activity)**
```json
{
  "run_id": "FALSE_POS_001",
  "koi_period": 1.2,        // Very short period (suspicious)
  "koi_duration": 1.8,      // Short duration
  "koi_depth": 15000.0,     // Very deep (too deep for planet)
  "koi_prad": 45.0,         // Unrealistically large
  "koi_teq": 2000.0,        // Extremely hot
  "koi_insol": 2000.0,      // Very high flux
  "koi_steff": 7000.0       // Hot star
}
```

## 🚀 **Steps to Run Your Predictions**

1. **Edit input.json** with your data:
   ```json
   {
     "predictions": [
       {
         "run_id": "MY_TEST_001",
         "koi_period": 10.5,
         "koi_duration": 3.2,
         "koi_depth": 500.0,
         "koi_prad": 1.8,
         "koi_teq": 700.0,
         "koi_insol": 50.0,
         "koi_steff": 5500.0
       }
     ]
   }
   ```

2. **Run the prediction script**:
   ```bash
   source venv/bin/activate
   python run_clean_predictions.py
   ```

3. **Check results** in `predictions_log.json`

## ⚠️ **Important Notes**

- **All 7 parameters are required** for each prediction
- **run_id must be unique** for each sample
- **Use realistic values** within the ranges shown above
- **Decimal numbers are allowed** (e.g., 10.5, 3.14159)
- **Very extreme values** might indicate false positives

## 🎯 **Quick Test**

Want to test with a simple example? Replace your input.json with:

```json
{
  "predictions": [
    {
      "run_id": "TEST_001",
      "koi_period": 10.0,
      "koi_duration": 3.0,
      "koi_depth": 500.0,
      "koi_prad": 2.0,
      "koi_teq": 600.0,
      "koi_insol": 25.0,
      "koi_steff": 5500.0
    }
  ]
}
```

This should predict an exoplanet with moderate confidence!