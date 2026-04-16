from db import fetch_logs, mark_as_processed
import joblib

model = joblib.load("model/model.pkl")

logs = fetch_logs()

# gör om till features
# prediction
# markera som processed
if anomaly_score > 0.8:
    send_alert("🚨 CRITICAL anomaly detected!")
elif anomaly_score > 0.6:
    send_alert("⚠️ Warning anomaly detected")