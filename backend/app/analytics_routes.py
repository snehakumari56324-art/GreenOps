from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import (
    CloudResource,
    HistoricalCloudResource
)

from .ml_service import detect_anomalies
from .kmeans_service import perform_kmeans
from .recommendation_service import generate_recommendations


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/overview")
def get_analytics_overview(
    db: Session = Depends(get_db)
):

    # --------------------------------
    # Current resources
    # --------------------------------

    current = db.query(
        CloudResource
    ).all()

    # --------------------------------
    # Historical training data
    # --------------------------------

    historical = db.query(
        HistoricalCloudResource
    ).all()

    # --------------------------------
    # No current resources
    # --------------------------------

    if not current:
        return {
            "total_resources": 0,
            "total_monthly_cost": 0,
            "total_carbon_emission": 0,
            "potential_monthly_saving": 0,
            "potential_carbon_reduction": 0
        }

    # --------------------------------
    # ACTUAL current cost
    # --------------------------------

    total_monthly_cost = sum(
        (resource.estimated_cost or 0)
        for resource in current
    )

    # --------------------------------
    # ACTUAL current carbon
    # --------------------------------

    total_carbon_emission = sum(
        (resource.carbon_emission or 0)
        for resource in current
    )

    # --------------------------------
    # ML analysis
    # --------------------------------

    anomaly_response = detect_anomalies(
        historical,
        current
    )

    if isinstance(anomaly_response, dict):
        anomaly_results = anomaly_response.get(
            "results",
            []
        )
    else:
        anomaly_results = anomaly_response

    # --------------------------------
    # K-Means
    # --------------------------------

    cluster_response = perform_kmeans(
        historical,
        current
    )

    if isinstance(cluster_response, dict):
        cluster_results = cluster_response.get(
            "clusters",
            []
        )
    else:
        cluster_results = cluster_response

    # --------------------------------
    # Recommendations
    # --------------------------------

    recommendations = generate_recommendations(
        current,
        anomaly_results,
        cluster_results
    )

    # --------------------------------
    # Potential monthly saving
    # --------------------------------

    potential_monthly_saving = sum(
        item.get(
            "estimated_monthly_saving",
            0
        )
        for item in recommendations
    )

    # --------------------------------
    # Potential carbon reduction
    # --------------------------------

    potential_carbon_reduction = sum(
        item.get(
            "estimated_carbon_reduction",
            0
        )
        for item in recommendations
    )

    # --------------------------------
    # Final response
    # --------------------------------

    return {
        "total_resources": len(current),

        "total_monthly_cost": round(
            total_monthly_cost,
            2
        ),

        "total_carbon_emission": round(
            total_carbon_emission,
            2
        ),

        "potential_monthly_saving": round(
            potential_monthly_saving,
            2
        ),

        "potential_carbon_reduction": round(
            potential_carbon_reduction,
            2
        )
    }