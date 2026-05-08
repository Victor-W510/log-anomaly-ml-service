import pandas as pd
from sklearn.ensemble import IsolationForest
import os
import joblib
from feature_engineering import feature_engineering

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "data", "training_data.json")
model_path = os.path.join(BASE_DIR, "model", "model.pkl")
columns_path = os.path.join(BASE_DIR, "model", "columns.pkl")

os.makedirs(os.path.dirname(model_path), exist_ok=True)
os.makedirs(os.path.dirname(columns_path), exist_ok=True)

data = pd.read_json(file_path)
x = feature_engineering(data)

model = IsolationForest()
model.fit(x)
columns = x.columns.to_list()
joblib.dump(model, model_path)
joblib.dump(columns,columns_path)


print(x)
