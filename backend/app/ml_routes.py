
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import (
    CloudResource,
    HistoricalCloudResource
)

from .ml_service import detect_anomalies
from .kmeans_service import perform_kmeans
from .regression_service import predict_cost


router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)


@router.get("/anomalies")
def get_anomalies(
    db: Session = Depends(get_db)
):

    historical = db.query(
        HistoricalCloudResource
    ).all()

    current = db.query(
        CloudResource
    ).all()

    return detect_anomalies(
        historical,
        current
    )


@router.get("/clusters")
def get_clusters(
    db: Session = Depends(get_db)
):

    historical = db.query(
        HistoricalCloudResource
    ).all()

    current = db.query(
        CloudResource
    ).all()

    return perform_kmeans(
        historical,
        current
    )


@router.get("/cost-prediction")
def get_cost_prediction(
    db: Session = Depends(get_db)
):

    historical = db.query(
        HistoricalCloudResource
    ).all()

    current = db.query(
        CloudResource
    ).all()

    return predict_cost(
        historical,
        current
    )
