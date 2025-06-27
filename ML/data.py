# from ucimlrepo import fetch_ucirepo 
  
# # fetch dataset 
# heart_disease = fetch_ucirepo(id=45) 
  
# # data (as pandas dataframes) 
# X = heart_disease.data.features 
# y = heart_disease.data.targets 
  
# # metadata 
# print(heart_disease.metadata) 
  
# # variable information 
# print(heart_disease.variables) 








import pandas as pd
from ucimlrepo import fetch_ucirepo

# Step 1: Fetch dataset (Heart Disease)
dataset = fetch_ucirepo(id=44)

# Step 2: Extract features and target
X = dataset.data.features
y = dataset.data.targets

# Step 3: Combine features and target into one DataFrame
df = pd.concat([X, y], axis=1)

# Step 4: Save as CSV
df.to_csv('heart_disease_dataset2.csv', index=False)

print("✅ Dataset saved as 'heart_disease_dataset2.csv'")
