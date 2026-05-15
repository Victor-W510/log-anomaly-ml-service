import requests
from dotenv import load_dotenv
import os

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_anomaly_alert(message):
    data = {
        "content":  "⚠️" + message
    }
    requests.post(WEBHOOK_URL, json=data)


def send_overload_alert():
    data = {
        "content": "📈 Unusual server activity detected!"
    }
    requests.post(WEBHOOK_URL, json=data)


def send_exception_alert(message):
    data = {
        "content":  "⛔️ Error in processing loop: "  + message
    }
    requests.post(WEBHOOK_URL, json=data)

# TEST
#send_overload_alert()




