from pydantic import BaseModel

class CloudResourceCreate(BaseModel):
    resource_id: str
    resource_type: str
    region: str | None = None
    instance_type: str | None = None
    status: str | None = "running"
    cpu_utilization: float = 0
    memory_utilization: float = 0
    estimated_cost: float = 0
    carbon_emission: float = 0
