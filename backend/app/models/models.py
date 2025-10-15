from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    forecasts = relationship("Forecast", back_populates="upload")

class Forecast(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"))
    forecast_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    upload = relationship("Upload", back_populates="forecasts")
    insights = relationship("Insight", back_populates="forecast")

class Insight(Base):
    __tablename__ = "insights"
    id = Column(Integer, primary_key=True, index=True)
    forecast_id = Column(Integer, ForeignKey("forecasts.id"))
    summary = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    forecast = relationship("Forecast", back_populates="insights")
