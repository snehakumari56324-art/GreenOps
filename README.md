# GreenOps — AI-Driven Cloud Cost, Energy & Carbon Optimization Platform

A college-project implementation based on the supplied GreenOps synopsis.

## Modules
- FastAPI backend
- MySQL database
- Cloud resource CRUD/read APIs
- Rule-based cost optimization recommendations
- Isolation Forest anomaly detection
- Demo AWS-like resource data (no AWS account required)
- React + Recharts dashboard
- Documentation

## Important
The AWS integration is intentionally left as an optional read-only module. The project can be demonstrated completely with local demo data.

## Backend
```powershell
cd backend
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env` from `.env.example`, then create the MySQL database/table using `docs/database.sql`.

Run:
```powershell
uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

## Frontend
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL shown in the terminal, normally http://localhost:5173.

## Demo data
Run:
```powershell
python scripts/seed_demo.py
```
This inserts six demo resources into MySQL through SQLAlchemy.

## GitHub
Do not commit `backend/.env`, AWS credentials, `venv`, or `node_modules`.
