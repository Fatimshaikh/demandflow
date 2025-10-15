# backend/app/routers/insights.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from app.core.deps import get_db
from app.models.models import Insight, Forecast

router = APIRouter()

# Load model once at startup
MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)

class InsightRequest(BaseModel):
    forecast_id: int
    context: str = "Generate a short natural language summary of this forecast."


@router.post("/insight/")
async def generate_insight(request: InsightRequest, db: Session = Depends(get_db)):
    forecast = db.query(Forecast).filter(Forecast.id == request.forecast_id).first()
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")

    forecast_data = forecast.forecast_data
    prompt = f"{request.context}\n\nForecast Data:\n{forecast_data}\n\nSummary:"

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True
    )

    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if "Summary:" in summary:
        summary = summary.split("Summary:")[-1].strip()

    new_insight = Insight(forecast_id=forecast.id, summary=summary)
    db.add(new_insight)
    db.commit()
    db.refresh(new_insight)

    return {"insight_id": new_insight.id, "insight": summary}


# ✅ NEW ENDPOINT: Fetch insight by forecast_id
@router.get("/insights/{forecast_id}")
def get_insight(forecast_id: int, db: Session = Depends(get_db)):
    insight = db.query(Insight).filter(Insight.forecast_id == forecast_id).first()
    return {"insight": insight.summary if insight else "No insight available yet."}
