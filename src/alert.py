import requests
from dotenv import load_dotenv
import os

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

#if anomaly_score > 0.8:
#    send_alert("🚨 CRITICAL anomaly detected!")
#elif anomaly_score > 0.6:
#    send_alert("⚠️ Warning anomaly detected")

def send_alert(message):
    data = {
        "content": message
    }

    requests.post(WEBHOOK_URL, json=data)


# TEST
send_alert("⚠️ Anomaly detected!")




