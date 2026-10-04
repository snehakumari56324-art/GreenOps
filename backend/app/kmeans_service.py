import pandas as pd
from sklearn.cluster import KMeans


def perform_kmeans(resources):
    if len(resources) < 3:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": "At least 3 resources are required for clustering."
        }

    data = []

    for resource in resources:
        data.append({
            "resource_id": resource.resource_id,
            "cpu_utilization": resource.cpu_utilization,
            "memory_utilization": resource.memory_utilization,
            "estimated_cost": resource.estimated_cost,
            "carbon_emission": resource.carbon_emission
        })

    df = pd.DataFrame(data)

    features = df[
        [
            "cpu_utilization",
            "memory_utilization",
            "estimated_cost",
            "carbon_emission"
        ]
    ]

    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    df["cluster"] = model.fit_predict(features)

    cluster_avg = df.groupby("cluster")[
        ["cpu_utilization", "memory_utilization"]
    ].mean()

    cluster_labels = {}

    for cluster_id, row in cluster_avg.iterrows():

        if row["cpu_utilization"] < 15:
            label = "LOW_UTILIZATION"
        elif row["cpu_utilization"] < 50:
            label = "MEDIUM_UTILIZATION"
        else:
            label = "HIGH_UTILIZATION"

        cluster_labels[cluster_id] = label

    df["utilization_level"] = df["cluster"].map(cluster_labels)

    return {
        "status": "SUCCESS",
        "clusters": df[
            [
                "resource_id",
                "cpu_utilization",
                "memory_utilization",
                "estimated_cost",
                "carbon_emission",
                "cluster",
                "utilization_level"
            ]
        ].to_dict(orient="records")
    }