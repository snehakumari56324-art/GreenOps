from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import (
    CloudResource,
    HistoricalCloudResource
)
from .data_service import get_current_resources


router = APIRouter(
    prefix="/data",
    tags=["Data Source"]
)


@router.post("/refresh")
def refresh_current_resources(
    db: Session = Depends(get_db)
):

    resources = get_current_resources()

    # Remove previous current snapshot
    db.query(CloudResource).delete()

    for item in resources:

        # -------------------------
        # CURRENT RESOURCE
        # -------------------------

        current_resource = CloudResource(
            resource_id=item["resource_id"],
            resource_type=item["resource_type"],
            region=item["region"],
            instance_type=item["instance_type"],
            status=item["status"],
            cpu_utilization=item["cpu_utilization"],
            memory_utilization=item["memory_utilization"],
            estimated_cost=item["estimated_cost"],
            carbon_emission=item["carbon_emission"]
        )

        db.add(current_resource)

        # -------------------------
        # HISTORICAL SNAPSHOT
        # -------------------------

        historical_resource = HistoricalCloudResource(
            resource_id=item["resource_id"],
            resource_type=item["resource_type"],
            region=item["region"],
            instance_type=item["instance_type"],
            status=item["status"],
            cpu_utilization=item["cpu_utilization"],
            memory_utilization=item["memory_utilization"],
            estimated_cost=item["estimated_cost"],
            carbon_emission=item["carbon_emission"],
            snapshot_at=item["snapshot_at"]
        )

        db.add(historical_resource)

    db.commit()

    return {
        "status": "SUCCESS",
        "data_source": "demo",
        "current_resources": len(resources),
        "message": "Current resource data refreshed successfully."
    }