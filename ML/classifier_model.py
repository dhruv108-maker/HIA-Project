from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from ucimlrepo import fetch_ucirepo
import pandas as pd
import joblib

# Fetch dataset
heart_disease = fetch_ucirepo(id=45)

# Get features and target
X = heart_disease.data.features
y = heart_disease.data.targets

# Convert target to binary: 0 = no disease, 1 = disease
y['target'] = y['num'].apply(lambda val: 1 if val > 0 else 0)

# Drop rows with missing values in features or target
data = pd.concat([X, y['target']], axis=1).dropna()
X = data.drop(columns='target')
y = data['target']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Results
print(classification_report(y_test, y_pred))
print(f'Accuracy Score: {model.score(X_test, y_test)}')


joblib.dump(model, 'ML/TrainedModels/heart_disease_model.joblib')

# import pandas as pd
# from ucimlrepo import fetch_ucirepo

# # Step 1: Fetch dataset (Heart Disease)
# dataset = fetch_ucirepo(id=45)

# # Step 2: Extract features and target
# X = dataset.data.features
# y = dataset.data.targets

# # Step 3: Combine features and target into one DataFrame
# df = pd.concat([X, y], axis=1)

# # Step 4: Save as CSV
# df.to_csv('heart_disease_dataset.csv', index=False)

# print("✅ Dataset saved as 'heart_disease_dataset.csv'")
