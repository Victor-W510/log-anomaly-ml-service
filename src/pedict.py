from db import get_connection, fetch_logs, mark_as_processed
from alert import send_alert
from feature_engineering import feature_engineering
import joblib
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(BASE_DIR, "model", "model.pkl")
model = joblib.load(model_path)

rates = []
last_alert_time = 0
ALERT_COOLDOWN = 60 

while True:
    connection = None
    try:
        connection = get_connection()
        logs = fetch_logs(connection, limit=100)

        if not logs:
            sleep_time = 60
            time.sleep(sleep_time)
            continue


        x = feature_engineering(logs)
        predictions = model.predict(x)

        current_rate = len(logs)
        
        rates.append(current_rate)
        
        if len(rates) > 50:
            rates.pop(0)

        avg_rate = sum(rates) / len(rates)
        std_rate = (sum((r - avg_rate) ** 2 for r in rates) / len(rates)) ** 0.5

        if std_rate > 0:
            z_score = (current_rate - avg_rate) / std_rate
        else:
            z_score = 0

        current_time = time.time()

        #so that we do not get to many alerts 
        if z_score > 3 and (current_time - last_alert_time > ALERT_COOLDOWN):
            send_alert()
            last_alert_time = current_time

        anomaly_ids = [
            log["id"]
            for log, pred in zip(logs, predictions)
            if pred == -1
            # send alert
        ]

        all_ids = [log["id"] for log in logs]
        mark_as_processed(connection, all_ids)

        print(f"Processed {len(logs)} logs, anomalies: {len(anomaly_ids)}")

    except Exception as e:
        #send alert
        print("Error in processing loop:", e)

    finally:
        if connection:
            connection.close()

    sleep_time = 10
    time.sleep(sleep_time)


