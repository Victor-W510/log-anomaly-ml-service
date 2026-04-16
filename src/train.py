import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# 1. Läs data
data = pd.read_csv("train.csv")

# 2. Välj features
X = data[["response_time"]]

# 3. Träna modell
model = IsolationForest()
model.fit(X)

# 4. Spara modell
joblib.dump(model, "model.pkl")

print("Model trained!")