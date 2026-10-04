# GreenOps — AI-Driven Cloud Cost, Energy & Carbon Optimization Platform

GreenOps is a college project designed to monitor cloud resources and identify opportunities for cloud cost optimization, resource utilization improvement, and carbon-emission reduction.

The platform combines a FastAPI backend, MySQL database, React dashboard, and Machine Learning models to analyze cloud-resource data and generate optimization recommendations.

## 🚀 Key Features

- Cloud resource monitoring dashboard
- Cloud cost analysis and optimization
- Carbon-emission estimation and reduction analysis
- Isolation Forest anomaly detection
- K-Means resource clustering
- AI-based optimization recommendations
- Admin approval/rejection workflow
- Approval history
- Cost and carbon analytics
- Resource utilization visualization
- MySQL-based resource storage
- FastAPI REST APIs
- React + Recharts dashboard
- Optional AWS read-only integration

## 🏗️ Project Architecture

```text
                 AWS / Demo Resources
                         |
                         v
              +----------------------+
              |   Data Collection    |
              | CloudWatch / Demo    |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |   FastAPI Backend    |
              |     REST APIs        |
              +----------+-----------+
                         |
              +----------+----------+
              |                     |
              v                     v
       +-------------+       +---------------+
       |    MySQL    |       |  ML Analysis  |
       |  Database   |       | IF + K-Means  |
       +-------------+       +-------+-------+
                                     |
                                     v
                          +--------------------+
                          | Recommendation     |
                          |     Engine         |
                          +---------+----------+
                                    |
                                    v
                          +--------------------+
                          | React Dashboard    |
                          |  Visualization     |
                          +---------+----------+
                                    |
                                    v
                          +--------------------+
                          | Approval / Reject  |
                          +--------------------+ '''

🧩 Project Modules
1. Resource Monitoring
The system stores and displays cloud-resource information including:
- Resource ID
- Resource type
- AWS region
- Instance type
- Resource status
- CPU utilization
- Memory utilization
- Estimated monthly cost
- Estimated carbon emission
2. Cost Optimization
The system analyzes resource utilization and identifies underutilized resources.
Possible recommendations include:
- Stop highly underutilized resources
- Consider downsizing resources
- Continue monitoring normally utilized resources
The dashboard displays the estimated potential monthly saving.
Note: Current cost values are project/demo estimates and are not direct AWS billing values.

3. Carbon Analysis
GreenOps estimates carbon emissions associated with the stored resource data and calculates potential carbon reduction based on recommended optimization actions.
Note: Current carbon values are project estimates for demonstration purposes and are not official AWS carbon-accounting measurements.

4. Isolation Forest
Isolation Forest is used to detect unusual or anomalous resource behavior.
The model analyzes:
- CPU utilization
- Memory utilization
- Estimated cost
- Carbon emission
Resources are classified as normal or anomalous based on the model output.
5. K-Means Clustering
K-Means groups resources according to their utilization and cost/carbon characteristics.
The current implementation classifies resources into:
- LOW_UTILIZATION
- MEDIUM_UTILIZATION
- HIGH_UTILIZATION
This helps the recommendation engine identify resources that may require optimization.
6. Recommendation Engine
The recommendation engine combines:
- CPU utilization
- K-Means utilization level
- Isolation Forest anomaly status
- Estimated cost
- Carbon emission
It generates:
- Priority
- Recommendation
- Reason
- Estimated monthly saving
- Estimated carbon reduction
7. Approval System
Optimization recommendations can be reviewed through the dashboard.
An administrator can:
- Approve a recommendation
- Reject a recommendation
- View approval history
The current approval system records the decision but does not automatically stop or modify real AWS resources.
🛠️ Technology Stack
Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Boto3
- Uvicorn
Database
- MySQL
Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Isolation Forest
- K-Means
Frontend
- React.js
- Vite
- Recharts
- CSS
Cloud
- AWS
- AWS EC2
- AWS CloudWatch
- Boto3
📁 Project Structure
GreenOps/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── resource_routes.py
│   │   ├── ml_service.py
│   │   ├── ml_routes.py
│   │   ├── kmeans_service.py
│   │   ├── kmeans_routes.py
│   │   ├── recommendation_service.py
│   │   ├── recommendation_routes.py
│   │   ├── analytics_routes.py
│   │   ├── aws_service.py
│   │   ├── aws_routes.py
│   │   └── approval_routes.py
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── style.css
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── scripts/
│   └── seed_demo.py
│
├── docs/
│   ├── database.sql
│   ├── architecture.txt
│   └── project_modules.md
│
├── screenshots/
│
├── .gitignore
└── README.md

⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/snehakumari56324-art/GreenOps.git
cd GreenOps

2. Backend Setup
cd backend

Create a virtual environment:
python -m venv venv

Activate the virtual environment:
.\venv\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

3. Configure Environment Variables
Create a .env file inside the backend folder.
Example:
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=greenops

Do not upload .env to GitHub.
Use .env.example as the template.
4. MySQL Database Setup
Create the database:
CREATE DATABASE greenops;

Then execute:
docs/database.sql

5. Insert Demo Data
From the project root:
python scripts\seed_demo.py

This inserts six demo cloud resources into MySQL.
6. Start the Backend
From the backend directory:
uvicorn app.main:app --reload

Backend:
http://127.0.0.1:8000

Swagger API documentation:
http://127.0.0.1:8000/docs

🎨 Frontend Setup
Open a new terminal.
From the project root:
cd frontend

Install dependencies:
npm install

Start the development server:
npm run dev

Open the Vite URL shown in the terminal.
Normally:
http://localhost:5173

📊 Dashboard
The dashboard provides:
- Total resource count
- Estimated monthly cost
- Total carbon emission
- Average CPU utilization
- Resource utilization charts
- AI optimization recommendations
- Potential monthly savings
- Potential carbon reduction
- Isolation Forest anomaly results
- K-Means clustering results
- Approval/rejection actions
- Approval history
- Cost vs. carbon analytics
🔌 API Endpoints
Resources
GET  /resources/
POST /resources/
GET  /resources/summary
GET  /resources/optimization

Machine Learning
GET /ml/anomalies
GET /ml/clusters

Recommendations
GET /recommendations/

Analytics
GET /analytics/overview

Approvals
GET  /approvals/
POST /approvals/

AWS
GET /aws/ec2

☁️ AWS Integration
AWS integration is implemented as an optional read-only module using Boto3.
The module can retrieve EC2 resource information such as:
- Instance ID
- Instance type
- Region
- Instance status
AWS credentials are not included in the repository.
The project can also run completely using local demo data without an AWS account.
🔐 Security
The following files and credentials must never be committed to GitHub:
backend/.env
AWS Access Keys
AWS Secret Keys
venv/
node_modules/
__pycache__/

The project .gitignore is configured to exclude sensitive and generated files.
📌 Current Project Status
Module	Status
MySQL Database	✅ Complete
FastAPI Backend	✅ Complete
React Dashboard	✅ Complete
Resource Monitoring	✅ Complete
Isolation Forest	✅ Complete
K-Means	✅ Complete
Recommendation Engine	✅ Complete
Approval System	✅ Complete
Cost Analytics	✅ Complete
Carbon Analytics	✅ Complete
AWS EC2 Integration	🔄 Optional / In Progress
CloudWatch Monitoring	🔄 Planned
Regression Model	🔄 Planned
Final Testing	🔄 Pending
Documentation & Report	🔄 Pending


🎯 Future Scope
Future improvements can include:
- Multi-cloud support for AWS, Azure and GCP
- Predictive autoscaling
- Real-time CloudWatch monitoring
- Automated resource optimization
- CI/CD integration
- Storage and network carbon accounting
- Advanced cost forecasting
- More sophisticated ML-based recommendations
👩‍💻 Project
GreenOps — AI-Driven Cloud Cost, Energy & Carbon Optimization Platform
A college project focused on combining Cloud Computing, Machine Learning, Cost Optimization, and Green Computing into a single monitoring and recommendation platform.