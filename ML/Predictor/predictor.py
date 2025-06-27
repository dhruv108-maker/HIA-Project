import joblib
import pandas as pd
from ucimlrepo import fetch_ucirepo

# Load the trained heart disease model
model = joblib.load('ML/TrainedModels/heart_disease_model.joblib')

# Load the SAME dataset it was trained on (ID 45 = Heart Disease)
heart_disease_dataset = fetch_ucirepo(id=45)
X = heart_disease_dataset.data.features

# Let's assume you want to predict for the first patient in the dataset
input_df = X.iloc[[0]]  # use double brackets to keep it as a DataFrame

# Make prediction
prediction = model.predict(input_df)[0]
probability = model.predict_proba(input_df)[0][1]

# Show result
if prediction == 1:
    print(f"⚠️ Heart Disease Risk Detected! Probability: {probability:.2%}")
else:
    print(f"✅ No Heart Disease Detected. Probability: {probability:.2%}")
