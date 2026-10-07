from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import CloudResource
from .regression_service import predict_cost


router = APIRouter(
    prefix="/ml",
    tags=["Regression ML"]
)


@router.get("/cost-prediction")
def get_cost_predictions(
    db: Session = Depends(get_db)
):
    resources = db.query(CloudResource).all()

    return predict_cost(resources)