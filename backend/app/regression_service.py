import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score


def predict_cost(
    historical_resources,
    current_resources
):

    if len(historical_resources) < 20:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": "At least 20 historical records are required."
        }

    if len(current_resources) == 0:
        return {
            "status": "NO_CURRENT_DATA",
            "predictions": []
        }

    historical_data = []

    for resource in historical_resources:

        historical_data.append({
            "cpu_utilization": resource.cpu_utilization or 0,
            "memory_utilization": resource.memory_utilization or 0,
            "carbon_emission": resource.carbon_emission or 0,
            "estimated_cost": resource.estimated_cost or 0
        })

    historical_df = pd.DataFrame(
        historical_data
    )

    features = [
        "cpu_utilization",
        "memory_utilization",
        "carbon_emission"
    ]

    X = historical_df[features]

    y = historical_df["estimated_cost"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    # Model evaluation
    cv_scores = cross_val_score(
        model,
        X,
        y,
        cv=5,
        scoring="r2"
    )

    # Final training
    model.fit(X, y)

    current_data = []

    for resource in current_resources:

        current_data.append({
            "resource_id": resource.resource_id,
            "cpu_utilization": resource.cpu_utilization or 0,
            "memory_utilization": resource.memory_utilization or 0,
            "carbon_emission": resource.carbon_emission or 0,
            "estimated_cost": resource.estimated_cost or 0
        })

    current_df = pd.DataFrame(
        current_data
    )

    predictions = model.predict(
        current_df[features]
    )

    results = []

    for i, resource in enumerate(current_resources):

        actual_cost = (
            resource.estimated_cost or 0
        )

        predicted_cost = float(
            predictions[i]
        )

        difference_percentage = (
            abs(
                actual_cost -
                predicted_cost
            ) / actual_cost * 100
            if actual_cost > 0
            else 0
        )

        if difference_percentage >= 10:

            difference_level = "HIGH"

        elif difference_percentage >= 5:

            difference_level = "MODERATE"

        else:

            difference_level = "NORMAL"

        results.append({
            "resource_id": resource.resource_id,

            "actual_cost": round(
                actual_cost,
                2
            ),

            "predicted_cost": round(
                predicted_cost,
                2
            ),

            "difference_percentage": round(
                difference_percentage,
                2
            ),

            "difference_level":
                difference_level
        })

    return {
        "status": "SUCCESS",
        "model": "Random Forest Regression",
        "training_records":
            len(historical_resources),

        "current_resources":
            len(current_resources),

        "r2_score": round(
            float(cv_scores.mean()),
            3
        ),

        "predictions": results
    }