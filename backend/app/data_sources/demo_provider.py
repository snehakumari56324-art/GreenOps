import random
from datetime import datetime


def get_current_resources():
    resources = []

    for i in range(1, 16):

        cpu = round(random.uniform(5, 95), 2)
        memory = round(random.uniform(10, 90), 2)

        instance_type = random.choice([
            "t3.small",
            "t3.medium",
            "t3.large"
        ])

        if instance_type == "t3.small":
            base_cost = 3000
            base_carbon = 13

        elif instance_type == "t3.medium":
            base_cost = 4500
            base_carbon = 20

        else:
            base_cost = 7000
            base_carbon = 32

        estimated_cost = round(
            base_cost * random.uniform(0.90, 1.10),
            2
        )

        carbon_emission = round(
            base_carbon * random.uniform(0.90, 1.10),
            2
        )

        resources.append({
            "resource_id": f"i-greenops-{i:03d}",
            "resource_type": "EC2",
            "region": "ap-south-1",
            "instance_type": instance_type,
            "status": "running",
            "cpu_utilization": cpu,
            "memory_utilization": memory,
            "estimated_cost": estimated_cost,
            "carbon_emission": carbon_emission,
            "snapshot_at": datetime.utcnow()
        })

    return resources