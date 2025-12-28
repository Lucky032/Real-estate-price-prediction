import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

print("Improved model training started")

# Load cleaned data
df = pd.read_excel("clean_real_estate_data.xlsx")
print("Data loaded:", df.shape)

# Separate encoders
area_le = LabelEncoder()
type_le = LabelEncoder()

df["Area"] = area_le.fit_transform(df["Area"])
df["Property_Type"] = type_le.fit_transform(df["Property_Type"])

# 🔹 LOG TRANSFORM TARGET (VERY EFFECTIVE)
df["Log_Price"] = np.log1p(df["Price_INR"])

# Features & target
X = df[["Year", "Area", "Property_Type", "Size_sqft"]]
y = df["Log_Price"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔹 TUNED RANDOM FOREST
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=18,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
r2 = r2_score(y_test, pred)
print("Improved Model R2 Score:", r2)

# Save model and encoders
pickle.dump(model, open("real_estate_model.pkl", "wb"))
pickle.dump(area_le, open("area_encoder.pkl", "wb"))
pickle.dump(type_le, open("type_encoder.pkl", "wb"))

print("Improved model and encoders saved successfully!")
