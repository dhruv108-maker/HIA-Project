import joblib
import pandas as pd

def heart_disease_predictor(file_path, patient_index=0):
    # Load the trained model
    model = joblib.load('ML/TrainedModels/heart_disease_model.joblib')

    # Load and clean dataset
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()

    # Drop target column if exists
    if 'num' in df.columns:
        df = df.drop(columns=['num'])

    # List of required features based on model training
    expected_features = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
        'restecg', 'thalach', 'exang', 'oldpeak',
        'slope', 'ca', 'thal'
    ]

    # Ensure required columns are present
    missing = [col for col in expected_features if col not in df.columns]
    if missing:
        print(f"⚠️ Error: Missing columns: {', '.join(missing)}")
        return

    # Arrange columns in the right order
    input_df = df[expected_features].iloc[[patient_index]]

    # Predict
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    # Output result
    if prediction == 1:
        print(f"⚠️ Heart Disease Risk Detected! Probability: {probability:.2%}")
    else:
        print(f"✅ No Heart Disease Detected. Probability: {probability:.2%}")

    return {
        "probability": probability
    }



# file_path = 'test_dataset.csv'

# heart_disease_predictor(file_path, patient_index=0)
