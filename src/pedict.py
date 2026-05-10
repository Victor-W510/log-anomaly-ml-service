from db import get_connection, fetch_logs, mark_as_processed
from alert import send_anomaly_alert, send_overload_alert, send_exception_alert
from feature_engineering import feature_engineering
import joblib
import time
import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(BASE_DIR, "model", "model.pkl")
columns_path = os.path.join(BASE_DIR, "model", "columns.pkl")
model = joblib.load(model_path)
columns_saved = joblib.load(columns_path)

rates = []
last_alert_time = 0
ALERT_COOLDOWN = 60 

def calculate_z (length): 
    rates.append(length)

    if len(rates) > 50:
        rates.pop(0)

    arr = np.array(rates, dtype=np.float64)

    avg = np.mean(arr)
    std_rate = np.std(arr)

    if std_rate > 0:
        z_score = (length - avg) / std_rate
    else:
        z_score = 0
    
    return z_score


def check_overload(z_score): 
    global last_alert_time
    current_time = time.time()

    #so that we do not get to many alerts 
    if (
        len(rates) >= 10 and 
        z_score > 3 and 
        (current_time - last_alert_time > ALERT_COOLDOWN)
        ):
        send_overload_alert()
        last_alert_time = current_time


while True:
    connection = None
    try:
        connection = get_connection()
        logs = fetch_logs(connection, limit=100)

        if not logs:
            time.sleep(60)
            continue

        df = pd.DataFrame(logs)
        x = feature_engineering(df)
        x = x.reindex(columns=columns_saved,fill_value=0)
        predictions = model.predict(x)


        z_score = calculate_z(len(logs))
        check_overload(z_score)

        anomaly = [
            log
            for log, pred in zip(logs, predictions)
            if pred == -1
        ]

        if anomaly:
            messages = "\n\n".join(
                (
                    f"Log ID: {i['id']}\n"
                    f"Level: {i['level']}\n"
                    f"Response Time: {i['response_time']} ms\n"
                    f"Message: {i['message']}"
                )
                for i in anomaly
            )

            send_anomaly_alert(
                f"{len(anomaly)} anomalies detected:\n{messages}"
            )

        all_ids = [log["id"] for log in logs]
        mark_as_processed(connection, all_ids)

        print(f"Processed {len(logs)} logs, anomalies: {len(anomaly)}")

    except Exception as e:
        send_exception_alert(str(e))
        print("Error in processing loop:", e)

    finally:
        if connection:
            connection.close()

    sleep_time = 10
    time.sleep(sleep_time)


