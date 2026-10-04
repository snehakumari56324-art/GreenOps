from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import CloudResource
from .schemas import CloudResourceCreate

router = APIRouter(prefix="/resources", tags=["Cloud Resources"])

@router.post("/")
def create_resource(resource: CloudResourceCreate, db: Session = Depends(get_db)):
    new_resource = CloudResource(**resource.model_dump())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return {"message": "Resource added successfully", "resource_id": new_resource.resource_id}

@router.get("/")
def get_resources(db: Session = Depends(get_db)):
    return db.query(CloudResource).all()

@router.get("/summary")
def resource_summary(db: Session = Depends(get_db)):
    resources = db.query(CloudResource).all()
    total_resources = len(resources)
    total_cost = sum(r.estimated_cost or 0 for r in resources)
    total_carbon = sum(r.carbon_emission or 0 for r in resources)
    average_cpu = (
        sum(r.cpu_utilization or 0 for r in resources) / total_resources
        if total_resources else 0
    )
    return {
        "total_resources": total_resources,
        "total_estimated_cost": round(total_cost, 2),
        "total_carbon_emission": round(total_carbon, 2),
        "average_cpu_utilization": round(average_cpu, 2)
    }

@router.get("/optimization")
def optimization_recommendations(db: Session = Depends(get_db)):
    resources = db.query(CloudResource).all()
    recommendations = []

    for resource in resources:
        cpu = resource.cpu_utilization or 0
        cost = resource.estimated_cost or 0

        if cpu < 10:
            saving = cost
            recommendations.append({
                "resource_id": resource.resource_id,
                "recommendation": "Consider stopping or downsizing this resource",
                "reason": f"Very low CPU utilization: {cpu}%",
                "priority": "HIGH",
                "estimated_monthly_saving": round(saving, 2)
            })
        elif cpu < 30:
            saving = cost * 0.30
            recommendations.append({
                "resource_id": resource.resource_id,
                "recommendation": "Consider downsizing this resource",
                "reason": f"Low CPU utilization: {cpu}%",
                "priority": "MEDIUM",
                "estimated_monthly_saving": round(saving, 2)
            })

    total_saving = sum(x["estimated_monthly_saving"] for x in recommendations)
    return {
        "total_recommendations": len(recommendations),
        "total_potential_monthly_saving": round(total_saving, 2),
        "recommendations": recommendations
    }
