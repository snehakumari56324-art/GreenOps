import gzip
import csv
from pathlib import Path

MAX_RESOURCES = 10000

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

OUTPUT_FILE = DATA_FOLDER / "public_greenops_data.csv"

files = list(DATA_FOLDER.glob("*.csv.gz"))

if not files:
    print("ERROR: No .csv.gz file found inside data folder.")
    exit()

DATA_FILE = files[0]

print("Using dataset:")
print(DATA_FILE)
print()

resources = {}

with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:

    reader = csv.reader(file)

    for row in reader:

        # Your dataset contains 5 columns
        if len(row) != 5:
            continue

        try:
            vm_id = row[1].strip()

            # Last column = average CPU value
            cpu = float(row[4])

            cpu = max(0, min(cpu, 100))

            if vm_id not in resources:

                # Derived values for GreenOps demo
                memory_utilization = max(5, min(95, cpu * 0.75))

                estimated_cost = 100 + (cpu * 10)

                carbon_emission = 5 + (cpu * 0.20)

                resources[vm_id] = {
                    "resource_id": vm_id,
                    "resource_type": "Azure VM",
                    "region": "Azure Public Dataset",
                    "instance_type": "Public VM",
                    "status": "running",
                    "cpu_utilization": round(cpu, 2),
                    "memory_utilization": round(
                        memory_utilization, 2
                    ),
                    "estimated_cost": round(
                        estimated_cost, 2
                    ),
                    "carbon_emission": round(
                        carbon_emission, 2
                    )
                }

        except (ValueError, IndexError):
            continue

        if len(resources) >= MAX_RESOURCES:
            break


with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as output:

    fieldnames = [
        "resource_id",
        "resource_type",
        "region",
        "instance_type",
        "status",
        "cpu_utilization",
        "memory_utilization",
        "estimated_cost",
        "carbon_emission"
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(resources.values())


print("----------------------------------------")
print("PUBLIC DATASET PROCESSING COMPLETE")
print("----------------------------------------")
print(f"Resources extracted: {len(resources)}")
print(f"Output file: {OUTPUT_FILE}")
print("----------------------------------------")