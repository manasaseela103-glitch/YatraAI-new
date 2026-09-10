from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TripRequest(BaseModel):
    destination: str = Field(..., example="Jaipur")
    dates: Optional[str] = Field(None, example="2026-10-15")
    days: int = Field(..., ge=1, le=30, example=3)
    travelers: int = Field(..., ge=1, example=2)
    budget: float = Field(..., ge=1000, example=35000)
    style: str = Field(..., example="Cultural")
    interests: List[str] = Field(default_factory=list, example=["History", "Food", "Culture"])


class Activity(BaseModel):
    time: str
    place: str
    activity: str
    description: str
    cost: str
    travel: str
    recommendation: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    category: Optional[str] = "Culture"


class DayPlan(BaseModel):
    day_number: int
    label: str
    date: str
    activities: List[Activity]


class BudgetBreakdown(BaseModel):
    accommodation: float
    food: float
    transport: float
    activities: float
    total: float


class TripResponse(BaseModel):
    id: str
    destination: str
    dates: Optional[str]
    days: int
    travelers: int
    budget: float
    style: str
    interests: List[str]
    days_plan: List[DayPlan]
    total_estimated_cost: float
    ai_insight: str
    budget_breakdown: BudgetBreakdown


class ReplanRequest(BaseModel):
    trip_id: Optional[str] = None
    scenario: str = Field(..., example="Attraction Closed")
    current_activity: Optional[Dict[str, Any]] = None
    destination: str = "Jaipur"
    days: int = 3
    travelers: int = 2
    budget: float = 35000
    interests: List[str] = Field(default_factory=list)


class ReplanResponse(BaseModel):
    scenario: str
    alert: str
    alternative: str
    time: str
    distance: str
    cost: str
    saved: str
    cost_diff: str
    reason: str
    why_list: List[str]
    new_activity: Activity


class AcceptReplanRequest(BaseModel):
    day_index: int = 0
    activity_index: int = 0
    new_activity: Activity


class DestinationItem(BaseModel):
    id: Optional[str] = None
    name: str
    region: str
    category: str
    rating: str
    description: str
    budget: str
    crowd: str
    image: str


class HiddenGemItem(BaseModel):
    id: Optional[str] = None
    place: str
    location: str
    why: str
    best: str
    crowd: str
    budget: str
    experience: str
    tag: str
    image: str


class ExperienceItem(BaseModel):
    id: Optional[str] = None
    type: str
    name: str
    provider: str
    location: str
    rating: str
    price: str
    description: str
    image: str


class BookingRequest(BaseModel):
    experience_name: str
    tourist_name: str
    email: str
    phone: str
    date: str
    travelers: int = 2
    notes: Optional[str] = None


class BusinessRegister(BaseModel):
    name: str
    category: str
    location: str
    rating: float = 5.0
    description: str
    contact_email: str
    phone: str
    address: str


class OfferItem(BaseModel):
    name: str
    discount: str
    validity: str
    active: bool = True


class SOSAlert(BaseModel):
    tourist_name: Optional[str] = "Traveler"
    location: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    emergency_type: str = "Medical / General SOS"
    contact_number: Optional[str] = None
    timestamp: Optional[str] = None


class BudgetOptimizeRequest(BaseModel):
    destination: str
    budget: float
    days: int
    travelers: int
    style: str


class UserProfile(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: str
    phone: Optional[str] = None
    preferences: List[str] = Field(default_factory=list)
