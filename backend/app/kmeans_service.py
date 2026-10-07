import pandas as pd
from sklearn.cluster import KMeans


def perform_kmeans(
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
            "clusters": []
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

    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
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

    current_df["cluster"] = model.predict(
        current_df[features]
    )

    cluster_avg = historical_df.copy()

    cluster_avg["cluster"] = model.labels_

    cluster_avg = cluster_avg.groupby(
        "cluster"
    )[[
        "cpu_utilization",
        "memory_utilization"
    ]].mean()

    cluster_labels = {}

    for cluster_id, row in cluster_avg.iterrows():

        if row["cpu_utilization"] < 15:

            label = "LOW_UTILIZATION"

        elif row["cpu_utilization"] < 50:

            label = "MEDIUM_UTILIZATION"

        else:

            label = "HIGH_UTILIZATION"

        cluster_labels[cluster_id] = label

    current_df["utilization_level"] = (
        current_df["cluster"]
        .map(cluster_labels)
    )

    return {
        "status": "SUCCESS",
        "model": "K-Means",
        "training_records": len(historical_resources),
        "current_resources": len(current_resources),
        "clusters": current_df[
            [
                "resource_id",
                "cpu_utilization",
                "memory_utilization",
                "estimated_cost",
                "carbon_emission",
                "cluster",
                "utilization_level"
            ]
        ].to_dict(
            orient="records"
        )
    }