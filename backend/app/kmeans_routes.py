from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import CloudResource
from .kmeans_service import perform_kmeans

router = APIRouter(
    prefix="/ml",
    tags=["K-Means ML"]
)


@router.get("/clusters")
def get_clusters(db: Session = Depends(get_db)):
    resources = db.query(CloudResource).all()

    result= perform_kmeans(resources)
    if isinstance(result, dict) and "clusters" in result:
        result["clusters"] = result["clusters"][:50]

    return result