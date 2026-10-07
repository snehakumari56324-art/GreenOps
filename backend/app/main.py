from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .resource_routes import router as resource_router
from .ml_routes import router as ml_router
from .aws_routes import router as aws_router
from .kmeans_routes import router as kmeans_router
from .recommendation_routes import router as recommendation_router
from .approval_routes import router as approval_router
from .analytics_routes import router as analytics_router
from .regression_routes import router as regression_router
from .data_routes import router as data_router

app = FastAPI(
    title="GreenOps",
    description="AI-Driven Cloud Cost, Energy and Carbon Optimization Platform",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resource_router)
app.include_router(ml_router)
app.include_router(aws_router)
app.include_router(kmeans_router)
app.include_router(recommendation_router)
app.include_router(approval_router)
app.include_router(analytics_router)
app.include_router(regression_router)
app.include_router(data_router)



@app.get("/")
def home():
    return {"message": "GreenOps Backend is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/db-test")
def database_test():
    try:
        connection = engine.connect()
        connection.close()
        return {"database": "connected", "status": "success"}
    except Exception as e:
        return {"database": "not connected", "error": str(e)}
