from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AQICategory(str, Enum):
    GOOD = "Good"
    MODERATE = "Moderate"
    POOR = "Poor"
    VERY_POOR = "Very Poor"
    SEVERE = "Severe"

class PollutionType(str, Enum):
    CONSTRUCTION = "Construction Dust"
    INDUSTRIAL = "Industrial Smoke"
    VEHICULAR = "Vehicular Emissions"
    BIOMASS = "Biomass Burning"
    GARBAGE = "Garbage Burning"
    OTHER = "Other"

class AQIReading(BaseModel):
    id: Optional[int] = None
    city: str = Field(..., min_length=1, max_length=100)
    aqi: float = Field(..., ge=0, le=999)
    pm25: Optional[float] = Field(None, ge=0)
    pm10: Optional[float] = Field(None, ge=0)
    no2: Optional[float] = Field(None, ge=0)
    so2: Optional[float] = Field(None, ge=0)
    co: Optional[float] = Field(None, ge=0)
    o3: Optional[float] = Field(None, ge=0)
    temp: Optional[float] = None
    humidity: Optional[float] = Field(None, ge=0, le=100)
    wind_speed: Optional[float] = Field(None, ge=0)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Delhi",
                "aqi": 267,
                "pm25": 145,
                "pm10": 280,
                "no2": 65,
                "so2": 18,
                "co": 2.3,
                "o3": 45,
                "lat": 28.7041,
                "lng": 77.1025
            }
        }

class PredictionRequest(BaseModel):
    city: str = Field(..., min_length=1)
    hours_ahead: int = Field(default=48, ge=1, le=72)
    include_confidence: bool = Field(default=True)

class PredictionResponse(BaseModel):
    city: str
    predictions: List[dict]
    model_accuracy: float
    confidence_interval: dict
    generated_at: datetime = Field(default_factory=datetime.now)

class CommunityReport(BaseModel):
    id: Optional[int] = None
    user_id: str = Field(..., min_length=1, max_length=100)
    user_name: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=200)
    pollution_type: PollutionType
    description: str = Field(..., max_length=1000)
    image_url: Optional[str] = Field(None, max_length=500)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    verified: bool = Field(default=False)
    votes: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "user_name": "Rahul Kumar",
                "location": "Connaught Place, Delhi",
                "pollution_type": "Construction Dust",
                "description": "Heavy construction dust from ongoing metro work",
                "lat": 28.6315,
                "lng": 77.2167
            }
        }

class ReportVerification(BaseModel):
    report_id: int
    verified_by: str
    verification_status: bool
    notes: Optional[str] = None

class PolicyImpact(BaseModel):
    id: Optional[int] = None
    policy_name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    implementation_date: datetime
    expected_reduction: float = Field(..., ge=0, le=100)
    actual_reduction: Optional[float] = Field(None, ge=0, le=100)
    status: str = Field(default="active")
    effectiveness_score: Optional[float] = Field(None, ge=0, le=100)
    city: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class HealthImpactResponse(BaseModel):
    city: str
    current_aqi: float
    health_risk_level: str
    estimated_daily_cases: dict
    economic_impact_cr: float
    vulnerable_population_pct: float
    health_advisory: str
    recommendations: List[str]

class SourceAttributionResponse(BaseModel):
    city: str
    sources: List[dict]
    primary_contributor: dict
    recommendations: List[str]
    confidence_score: float

class UserActivity(BaseModel):
    id: Optional[int] = None
    user_id: str
    action_type: str
    points_earned: int = Field(default=0, ge=0)
    metadata: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.now)

class UserProfile(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None
    total_points: int = Field(default=0, ge=0)
    level: int = Field(default=1, ge=1)
    achievements: List[str] = Field(default_factory=list)
    reports_submitted: int = Field(default=0, ge=0)
    reports_verified: int = Field(default=0, ge=0)
    joined_at: datetime = Field(default_factory=datetime.now)

class AlertSettings(BaseModel):
    user_id: str
    city: str
    aqi_threshold: float = Field(default=200, ge=0, le=500)
    notification_enabled: bool = Field(default=True)
    notification_channels: List[str] = Field(default=["email", "push"])

class HistoricalDataRequest(BaseModel):
    city: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    days: int = Field(default=30, ge=1, le=365)
    pollutants: Optional[List[str]] = None

class ComparisonRequest(BaseModel):
    cities: List[str] = Field(..., min_items=2, max_items=10)
    metric: str = Field(default="aqi")
    period_days: int = Field(default=7, ge=1, le=90)