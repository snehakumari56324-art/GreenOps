from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import CloudResource
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
    # Get all resources from database
    resources = db.query(CloudResource).all()

    if not resources:
        return {
            "status": "SUCCESS",
            "total_recommendations": 0,
            "total_potential_monthly_saving": 0,
            "total_potential_carbon_reduction": 0,
            "recommendations": []
        }

    # -----------------------------
    # Isolation Forest
    # -----------------------------
    anomaly_results = detect_anomalies(resources)

    # If the function returns a dictionary
    if isinstance(anomaly_results, dict):
        anomaly_results = anomaly_results.get(
            "results", []
        )

    # -----------------------------
    # K-Means
    # -----------------------------
    cluster_response = perform_kmeans(resources)

    if isinstance(cluster_response, dict):
        cluster_results = cluster_response.get(
            "clusters", []
        )
    else:
        cluster_results = cluster_response

    # -----------------------------
    # Recommendation Engine
    # -----------------------------
    recommendations = generate_recommendations(
        resources,
        anomaly_results,
        cluster_results
    )

    # -----------------------------
    # Total Cost Saving
    # -----------------------------
    total_saving = sum(
        item["estimated_monthly_saving"]
        for item in recommendations
    )

    # -----------------------------
    # Total Carbon Reduction
    # -----------------------------
    total_carbon_reduction = sum(
        item["estimated_carbon_reduction"]
        for item in recommendations
    )

    return {
        "status": "SUCCESS",
        "total_recommendations": len(
            recommendations
        ),
        "total_potential_monthly_saving": round(
            total_saving, 2
        ),
        "total_potential_carbon_reduction": round(
            total_carbon_reduction, 2
        ),
        "recommendations": recommendations
    }