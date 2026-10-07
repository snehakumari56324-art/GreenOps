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
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/")
def get_recommendations(
    db: Session = Depends(get_db)
):

    # --------------------------------
    # Get historical training data
    # --------------------------------

    historical = db.query(
        HistoricalCloudResource
    ).all()

    # --------------------------------
    # Get current resources
    # --------------------------------

    current = db.query(
        CloudResource
    ).all()

    # --------------------------------
    # If no current resources exist
    # --------------------------------

    if not current:
        return {
            "status": "SUCCESS",
            "training_records": len(historical),
            "current_resources": 0,
            "total_recommendations": 0,
            "total_potential_monthly_saving": 0,
            "total_potential_carbon_reduction": 0,
            "recommendations": []
        }

    # --------------------------------
    # Isolation Forest
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
    # Recommendation Engine
    # --------------------------------

    recommendations = generate_recommendations(
        current,
        anomaly_results,
        cluster_results
    )

    # --------------------------------
    # Total Cost Saving
    # --------------------------------

    total_saving = sum(
        item.get(
            "estimated_monthly_saving",
            0
        )
        for item in recommendations
    )

    # --------------------------------
    # Total Carbon Reduction
    # --------------------------------

    total_carbon_reduction = sum(
        item.get(
            "estimated_carbon_reduction",
            0
        )
        for item in recommendations
    )

    # --------------------------------
    # Final Response
    # --------------------------------

    return {
        "status": "SUCCESS",

        "training_records": len(
            historical
        ),

        "current_resources": len(
            current
        ),

        "total_recommendations": len(
            recommendations
        ),

        "total_potential_monthly_saving": round(
            total_saving,
            2
        ),

        "total_potential_carbon_reduction": round(
            total_carbon_reduction,
            2
        ),

        "recommendations": recommendations
    }