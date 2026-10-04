# GreenOps Project Modules

## 1. Resource Monitoring
FastAPI reads cloud-resource records from MySQL.

## 2. Optimization
Low CPU utilization generates recommendations:
- below 10%: HIGH priority
- below 30%: MEDIUM priority

The saving values are project estimates based on the stored `estimated_cost` field.

## 3. Machine Learning
Isolation Forest analyzes CPU, memory, estimated cost and carbon-emission fields to flag unusual resource patterns.

## 4. AWS Integration
Boto3 can read EC2 instances through `/aws/ec2`. It is read-only and optional for the local demonstration.

## 5. Dashboard
React + Recharts displays:
- total resources
- estimated cost
- carbon estimate
- average CPU
- utilization chart
- optimization recommendations
- ML anomaly results

## Limitations
Actual AWS billing, CloudWatch memory metrics and official carbon accounting are not implemented in the local demo. These require additional AWS configuration and documented measurement methodology.
