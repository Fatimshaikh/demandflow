# backend/app/routers/forecast.py

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pandas as pd
from prophet import Prophet
from app.core.deps import get_db
from app.models.models import Upload, Forecast
import json

router = APIRouter()

class ForecastRequest(BaseModel):
    data: list
    date_column: str
    value_column: str
    periods: int = 30

@router.post("/forecast/")
async def generate_forecast(request: ForecastRequest, db: Session = Depends(get_db)):
    df = pd.DataFrame(request.data)

    if request.date_column not in df.columns or request.value_column not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid column names")

    df = df[[request.date_column, request.value_column]]
    df = df.rename(columns={request.date_column: "ds", request.value_column: "y"})

    try:
        model = Prophet()
        model.fit(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error training model: {e}")

    future = model.make_future_dataframe(periods=request.periods)
    forecast = model.predict(future)

    result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(request.periods).to_dict(orient="records")

    # Save forecast in DB
    new_upload = Upload(filename="uploaded_from_api")
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)

    forecast_entry = Forecast(upload_id=new_upload.id, forecast_data=json.dumps(result))
    db.add(forecast_entry)
    db.commit()
    db.refresh(forecast_entry)

    return {
        "forecast_id": forecast_entry.id,
        "message": f"Forecast generated for next {request.periods} days",
        "forecast": result
    }


# ✅ NEW ENDPOINT: Fetch all forecasts
@router.get("/forecasts/")
def get_forecasts(db: Session = Depends(get_db)):
    forecasts = db.query(Forecast).all()
    return [
        {
            "id": f.id,
            "upload": {"filename": f.upload.filename if f.upload else None},
            "forecast_data": f.forecast_data,
            # optional: only include if you have created_at column in your model
            "created_at": getattr(f, "created_at", None)
        }
        for f in forecasts
    ]
