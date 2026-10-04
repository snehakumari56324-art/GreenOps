from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Approval

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)


# Get approval history
@router.get("/")
def get_approvals(db: Session = Depends(get_db)):
    return db.query(Approval).order_by(
        Approval.created_at.desc()
    ).all()


# Create approval / rejection
@router.post("/")
def create_approval(
    resource_id: str,
    action: str,
    status: str,
    db: Session = Depends(get_db)
):

    if status not in ["APPROVED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be APPROVED or REJECTED"
        )

    approval = Approval(
        resource_id=resource_id,
        action=action,
        approved=True if status == "APPROVED" else False,
        status=status
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return approval