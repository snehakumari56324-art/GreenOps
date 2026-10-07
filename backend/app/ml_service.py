import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(
    historical_resources,
    current_resources
):

    if len(historical_resources) < 10:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": "At least 10 historical records are required."
        }

    if len(current_resources) == 0:
        return {
            "status": "NO_CURRENT_DATA",
            "results": []
        }

    historical_data = []

    for resource in historical_resources:

        historical_data.append({
            "cpu_utilization": resource.cpu_utilization or 0,
            "memory_utilization": resource.memory_utilization or 0,
            "estimated_cost": resource.estimated_cost or 0,
            "carbon_emission": resource.carbon_emission or 0
        })

    historical_df = pd.DataFrame(
        historical_data
    )

    features = [
        "cpu_utilization",
        "memory_utilization",
        "estimated_cost",
        "carbon_emission"
    ]

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    model.fit(
        historical_df[features]
    )

    current_data = []

    for resource in current_resources:

        current_data.append({
            "resource_id": resource.resource_id,
            "cpu_utilization": resource.cpu_utilization or 0,
            "memory_utilization": resource.memory_utilization or 0,
            "estimated_cost": resource.estimated_cost or 0,
            "carbon_emission": resource.carbon_emission or 0
        })

    current_df = pd.DataFrame(
        current_data
    )

    predictions = model.predict(
        current_df[features]
    )

    results = []

    for i, resource in enumerate(current_resources):

        label = (
            "ANOMALY"
            if predictions[i] == -1
            else "NORMAL"
        )

        results.append({
            "resource_id": resource.resource_id,
            "anomaly_label": label,
            "cpu_utilization": resource.cpu_utilization,
            "memory_utilization": resource.memory_utilization,
            "estimated_cost": resource.estimated_cost,
            "carbon_emission": resource.carbon_emission
        })

    return {
        "status": "SUCCESS",
        "model": "Isolation Forest",
        "training_records": len(historical_resources),
        "current_resources": len(current_resources),
        "results": results
    }
