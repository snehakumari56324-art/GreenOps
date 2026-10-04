def generate_recommendations(resources, anomaly_results, cluster_results):
    recommendations = []

    # Create quick lookup for ML results
    anomaly_map = {
        item["resource_id"]: item
        for item in anomaly_results
    }

    cluster_map = {
        item["resource_id"]: item
        for item in cluster_results
    }

    for resource in resources:
        resource_id = resource.resource_id

        cpu = resource.cpu_utilization or 0
        memory = resource.memory_utilization or 0
        cost = resource.estimated_cost or 0
        carbon = resource.carbon_emission or 0

        anomaly = anomaly_map.get(resource_id, {})
        cluster = cluster_map.get(resource_id, {})

        anomaly_label = anomaly.get(
            "anomaly_label",
            "NORMAL"
        )

        utilization_level = cluster.get(
            "utilization_level",
            "UNKNOWN"
        )

        # Default values
        priority = "LOW"
        recommendation = "Continue monitoring the resource."
        reason = "Resource utilization is within an acceptable range."

        # HIGH priority
        if (
            cpu < 10
            or utilization_level == "LOW_UTILIZATION"
            or anomaly_label == "ANOMALY"
        ):
            priority = "HIGH"

            recommendation = (
                "Consider stopping or downsizing this resource."
            )

            reason = (
                f"Low CPU utilization ({cpu}%), "
                f"utilization level is {utilization_level}, "
                f"and estimated monthly cost is ₹{cost}."
            )

        # MEDIUM priority
        elif (
            cpu < 30
            or utilization_level == "MEDIUM_UTILIZATION"
        ):
            priority = "MEDIUM"

            recommendation = (
                "Consider right-sizing this resource "
                "to reduce unnecessary usage."
            )

            reason = (
                f"CPU utilization is {cpu}% and "
                f"the resource is classified as "
                f"{utilization_level}."
            )

        # Estimated savings
        if priority == "HIGH":
            estimated_saving = cost
        elif priority == "MEDIUM":
            estimated_saving = cost * 0.30
        else:
            estimated_saving = 0

        # Estimated carbon reduction
        if cost > 0:
            carbon_reduction = (
                carbon * (estimated_saving / cost)
            )
        else:
            carbon_reduction = 0

        recommendations.append({
            "resource_id": resource_id,
            "priority": priority,
            "recommendation": recommendation,
            "reason": reason,
            "estimated_monthly_saving": round(
                estimated_saving, 2
            ),
            "estimated_carbon_reduction": round(
                carbon_reduction, 2
            ),
            "anomaly_status": anomaly_label,
            "utilization_level": utilization_level
        })

    return recommendations