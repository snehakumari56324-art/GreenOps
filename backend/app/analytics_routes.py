from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import CloudResource


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/overview")
def get_analytics_overview(
    db: Session = Depends(get_db)
):
    resources = db.query(CloudResource).all()

    total_cost = sum(
        r.estimated_cost or 0
        for r in resources
    )

    total_carbon = sum(
        r.carbon_emission or 0
        for r in resources
    )

    low_utilization = [
        r for r in resources
        if (r.cpu_utilization or 0) < 10
    ]

    potential_saving = sum(
        r.estimated_cost or 0
        for r in low_utilization
    )

    potential_carbon_reduction = sum(
        r.carbon_emission or 0
        for r in low_utilization
    )

    return {
        "total_resources": len(resources),
        "total_monthly_cost": round(total_cost, 2),
        "total_carbon_emission": round(total_carbon, 2),
        "potential_monthly_saving": round(
            potential_saving, 2
        ),
        "potential_carbon_reduction": round(
            potential_carbon_reduction, 2
        )
    }