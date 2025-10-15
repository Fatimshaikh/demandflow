from fastapi import FastAPI
from app.routers import upload, forecast, insights

app = FastAPI()

app.include_router(upload.router, prefix="/api")
app.include_router(forecast.router, prefix="/api")
app.include_router(insights.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "DemandFlow Backend is running successfully 🚀"}
