from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import CloudResource
from .ml_service import detect_anomalies

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

@router.get("/anomalies")
def get_anomalies(db: Session = Depends(get_db)):
    resources = db.query(CloudResource).all()
    results = detect_anomalies(resources)
    anomaly_count = sum(1 for x in results if x["anomaly_label"] == "ANOMALY")
    return {
        "algorithm": "Isolation Forest",
        "total_resources": len(results),
        "anomalies_detected": anomaly_count,
        "results": results
    }
