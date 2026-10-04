from fastapi import APIRouter, HTTPException
from .aws_service import get_ec2_resources

router = APIRouter(prefix="/aws", tags=["AWS Cloud"])

@router.get("/ec2")
def get_aws_ec2(region="ap-south-1"):
    try:
        resources = get_ec2_resources(region)
        return {"region": region, "total_instances": len(resources), "resources": resources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
