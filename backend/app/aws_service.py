import boto3

def get_ec2_resources(region="ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances()
    resources = []

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            resources.append({
                "resource_id": instance.get("InstanceId"),
                "resource_type": "EC2",
                "region": region,
                "instance_type": instance.get("InstanceType"),
                "status": instance.get("State", {}).get("Name", "unknown")
            })
    return resources
