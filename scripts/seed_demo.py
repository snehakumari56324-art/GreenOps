import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from app.database import SessionLocal
from app.models import CloudResource

demo = [
    ("i-greenops-001", 8.5, 15.2, 450, 12.5),
    ("i-greenops-002", 78, 65, 1200, 35),
    ("i-greenops-003", 12, 18, 450, 12.5),
    ("i-greenops-004", 92, 85, 2400, 60),
    ("i-greenops-005", 22, 25, 600, 18),
    ("i-greenops-006", 6, 10, 500, 15),
]

db = SessionLocal()
try:
    for rid, cpu, mem, cost, carbon in demo:
        existing = db.query(CloudResource).filter_by(resource_id=rid).first()
        if existing:
            continue
        db.add(CloudResource(
            resource_id=rid,
            resource_type="EC2",
            region="ap-south-1",
            instance_type="t2.micro",
            status="running",
            cpu_utilization=cpu,
            memory_utilization=mem,
            estimated_cost=cost,
            carbon_emission=carbon
        ))
    db.commit()
    print("Demo resources inserted.")
finally:
    db.close()
