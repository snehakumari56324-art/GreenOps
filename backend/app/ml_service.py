import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(resources):
    if not resources:
        return []

    data = [{
        "resource_id": r.resource_id,
        "cpu_utilization": r.cpu_utilization or 0,
        "memory_utilization": r.memory_utilization or 0,
        "estimated_cost": r.estimated_cost or 0,
        "carbon_emission": r.carbon_emission or 0
    } for r in resources]

    df = pd.DataFrame(data)

    if len(df) < 2:
        for item in data:
            item["anomaly"] = 0
            item["anomaly_score"] = None
            item["anomaly_label"] = "INSUFFICIENT_DATA"
        return data

    features = ["cpu_utilization", "memory_utilization", "estimated_cost", "carbon_emission"]
    contamination = min(0.25, max(1 / len(df), 0.01))

    model = IsolationForest(contamination=contamination, random_state=42)
    predictions = model.fit_predict(df[features])
    scores = model.decision_function(df[features])

    results = []
    for i, item in enumerate(data):
        prediction = int(predictions[i])
        results.append({
            **item,
            "anomaly": prediction,
            "anomaly_score": round(float(scores[i]), 4),
            "anomaly_label": "ANOMALY" if prediction == -1 else "NORMAL"
        })
    return results
