from typing import Any

from pydantic import BaseModel, Field


class TripPlanRequest(BaseModel):
    destination: str
    days: int = Field(..., ge=1, le=30)
    travelers: int = Field(..., ge=1)
    budget: float = Field(..., gt=0)
    travel_style: str
    interests: list[str]


class TripPlanResponse(BaseModel):
    trip_id: str | None = None
    destination: str
    days: int
    travelers: int
    budget: float
    travel_style: str
    interests: list[str]
    itinerary: list[dict[str, Any]]
    budget_breakdown: dict[str, Any]
    ai_insight: str
    places: list[dict[str, Any]] = Field(default_factory=list)


class ReplanRequest(BaseModel):
    current_itinerary: list[dict[str, Any]] = Field(default_factory=list)
    scenario: str
    trip_id: str | None = None
    destination: str = "your destination"
    days: int = 3
    travelers: int = 1
    budget: float | None = None
    interests: list[str] = Field(default_factory=list)
    current_activity: dict[str, Any] | None = None


class ReplanResponse(BaseModel):
    trip_id: str | None = None
    alert: str
    reason: str
    recommended_changes: list[str]
    updated_itinerary: list[dict[str, Any]]
    budget_impact: dict[str, Any]
    ai_insight: str
    alternative: str | None = None
    time: str | None = None
    distance: str | None = None
    cost: str | None = None
    saved: str | None = None
    cost_diff: str | None = None
    why_list: list[str] = Field(default_factory=list)
    new_activity: dict[str, Any] | None = None
    recommended_places: list[dict[str, Any]] = Field(default_factory=list)
