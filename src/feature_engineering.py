import pandas as pd


def map_thread(thread_name):
    thread_name = str(thread_name).strip().lower()
    
    if "http" in thread_name:
        return "http"
    elif "task" in thread_name or "pool" in thread_name:
        return "worker"
    elif "main" in thread_name:
        return "main"
    else:
        return "other"

def feature_engineering(logs):
    
    df = pd.DataFrame(logs)

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=False, errors="coerce")
    df["hour"] = df["timestamp"].dt.hour.fillna(0)
    
    df["message_length"] = df["message"].astype(str).str.strip().apply(len)

    df["thread"] = df["thread"].apply(map_thread)

    df["responseTime"] = pd.to_numeric(df["responseTime"],errors="coerce").fillna(0)

    level_dummies = pd.get_dummies(df["level"].str.strip())
    thread_dummies = pd.get_dummies(df["thread"])

    features = pd.concat([
        level_dummies,
        thread_dummies,
        df[[ "message_length", "hour", "responseTime"]] 
    ], axis=1)

    return features