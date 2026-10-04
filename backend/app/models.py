from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    TIMESTAMP,
    func
)
from sqlalchemy.sql import func
from .database import Base

class CloudResource(Base):
    __tablename__ = "cloud_resources"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    resource_type = Column(String(50), nullable=False)
    region = Column(String(50))
    instance_type = Column(String(50))
    status = Column(String(30))
    cpu_utilization = Column(Float, default=0)
    memory_utilization = Column(Float, default=0)
    estimated_cost = Column(Float, default=0)
    carbon_emission = Column(Float, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(String(100), nullable=False)
    action = Column(String(255), nullable=False)
    approved = Column(Boolean, nullable=False)
    status = Column(String(30), nullable=False)
    created_at = Column(
        DateTime,
        server_default=func.now()
    )