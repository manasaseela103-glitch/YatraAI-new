from typing import Union
from fastapi import APIRouter, HTTPException, Path
from models import TripRequest, TripResponse, AcceptReplanRequest
from schemas import ReplanRequest, ReplanResponse, TripPlanRequest, TripPlanResponse
from ai_service import generate_itinerary
import database
from copy import deepcopy
from places_service import search_places

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("/plan", response_model=TripPlanResponse)
async def plan_trip(req: TripPlanRequest):
    try:
        interests = req.interests or ["local highlights"]
        itinerary = []

        for day in range(1, req.days + 1):
            interest = interests[(day - 1) % len(interests)]
            itinerary.append({
                "day": day,
                "morning": f"Explore {req.destination}'s {interest} highlights",
                "afternoon": f"Enjoy a {req.travel_style.lower()} experience in {req.destination}",
                "evening": f"Discover local food and culture in {req.destination}",
            })

        budget_breakdown = {
            "accommodation": round(req.budget * 0.4, 2),
            "food": round(req.budget * 0.2, 2),
            "transport": round(req.budget * 0.15, 2),
            "activities": round(req.budget * 0.25, 2),
        }

        places = await search_places(req.destination, req.interests, req.budget)

        trip = TripPlanResponse(
            destination=req.destination,
            days=req.days,
            travelers=req.travelers,
            budget=req.budget,
            travel_style=req.travel_style,
            interests=req.interests,
            itinerary=itinerary,
            budget_breakdown=budget_breakdown,
            ai_insight=(
                f"This {req.days}-day {req.travel_style.lower()} plan for {req.travelers} "
                f"traveler(s) in {req.destination} is tailored around your interests."
            ),
            places=places,
        )
        trip_id = await database.save_trip(trip.model_dump())
        trip.trip_id = trip_id
        await database.update_trip(trip_id, {"trip_id": trip_id})
        return trip
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to plan trip: {str(e)}")


@router.post("/generate", response_model=TripResponse)
async def create_trip(req: TripRequest):
    try:
        trip = await generate_itinerary(req)
        await database.save_trip(trip.model_dump())
        return trip
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate trip: {str(e)}")


@router.get("/{trip_id}", response_model=Union[TripResponse, TripPlanResponse])
async def get_trip_by_id(trip_id: str = Path(...)):
    try:
        trip_data = await database.get_trip(trip_id)
        if not trip_data:
            raise HTTPException(status_code=404, detail="Trip not found")
        if "itinerary" in trip_data:
            return TripPlanResponse(**trip_data)
        return TripResponse(**trip_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve trip: {str(e)}")


@router.post("/replan", response_model=ReplanResponse)
async def replan_trip(req: ReplanRequest):
    scenario_key = {
        "attraction closed": "attraction_closed",
        "bad weather": "bad_weather",
        "heavy crowd": "heavy_crowd",
        "transport delay": "transport_delay",
        "budget exceeded": "budget_exceeded",
    }.get(req.scenario.lower(), req.scenario.lower())
    scenario_details = {
        "attraction_closed": {
            "alert": "Your planned attraction is closed",
            "reason": "The closed attraction has been replaced with a nearby experience.",
            "change": f"Explore an alternative local highlight in {req.destination}",
            "impact": 0,
        },
        "bad_weather": {
            "alert": "Bad weather is affecting your plan",
            "reason": "An indoor activity keeps the day comfortable without losing local character.",
            "change": f"Move your plans indoors in {req.destination}",
            "impact": 0,
        },
        "heavy_crowd": {
            "alert": "Heavy crowds are expected",
            "reason": "A quieter alternative gives you more time to explore at your own pace.",
            "change": f"Visit a less crowded neighborhood in {req.destination}",
            "impact": 0,
        },
        "transport_delay": {
            "alert": "A transport delay has been detected",
            "reason": "The itinerary has been adjusted to reduce transfers and protect your day.",
            "change": f"Choose a nearby stop in {req.destination}",
            "impact": -round((req.budget or 0) * 0.03, 2),
        },
        "budget_exceeded": {
            "alert": "The current plan exceeds your budget",
            "reason": "A lower-cost alternative keeps the experience while reducing spend.",
            "change": f"Switch to a budget-friendly experience in {req.destination}",
            "impact": -round((req.budget or 0) * 0.08, 2),
        },
    }.get(scenario_key)
    if not scenario_details:
        raise HTTPException(status_code=422, detail="Unsupported replan scenario")

    updated_itinerary = deepcopy(req.current_itinerary)
    replacement = scenario_details["change"]
    new_activity = {
        "time": "Morning",
        "place": replacement,
        "activity": replacement,
        "description": replacement,
        "cost": "Included",
        "travel": "Flexible",
        "recommendation": replacement,
    }
    if updated_itinerary:
        first_day = updated_itinerary[0]
        if all(slot in first_day for slot in ("morning", "afternoon", "evening")):
            first_day["morning"] = replacement
        elif first_day.get("activities"):
            first_day["activities"][0]["activity"] = replacement
            first_day["activities"][0]["description"] = replacement
            new_activity = first_day["activities"][0]
    elif req.current_activity:
        new_activity = {**req.current_activity, **new_activity}

    impact = scenario_details["impact"]
    response = ReplanResponse(
        trip_id=req.trip_id,
        alert=scenario_details["alert"],
        reason=scenario_details["reason"],
        recommended_changes=[replacement],
        updated_itinerary=updated_itinerary,
        budget_impact={
            "amount": impact,
            "direction": "saved" if impact < 0 else "unchanged",
            "summary": f"{abs(impact):.2f} saved" if impact < 0 else "No budget change",
        },
        ai_insight=f"Your {scenario_key.replace('_', ' ')} plan is adjusted to keep {req.destination} enjoyable and practical.",
        alternative=replacement,
        time="Morning",
        distance="Nearby",
        cost="Included",
        saved=f"{abs(impact):.2f}" if impact < 0 else "0",
        cost_diff=f"{impact:.2f}",
        why_list=[scenario_details["reason"]],
        new_activity=new_activity,
        recommended_places=await search_places(req.destination, req.interests, req.budget),
    )
    trip_record = {
        "destination": req.destination,
        "days": req.days,
        "travelers": req.travelers,
        "budget": req.budget or 0,
        "interests": req.interests,
        "itinerary": updated_itinerary,
        "updated_itinerary": updated_itinerary,
        "recommended_places": response.recommended_places,
        "scenario": scenario_key,
        "ai_insight": response.ai_insight,
    }
    if req.trip_id and await database.get_trip(req.trip_id):
        await database.update_trip(req.trip_id, trip_record)
        response.trip_id = req.trip_id
    else:
        response.trip_id = await database.save_trip(trip_record)
    return response


@router.put("/{trip_id}/accept-replan", response_model=TripResponse)
async def accept_replan(trip_id: str, req: AcceptReplanRequest):
    trip_data = await database.get_trip(trip_id)
    if not trip_data:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    days_plan = trip_data.get("days_plan", [])
    if 0 <= req.day_index < len(days_plan):
        activities = days_plan[req.day_index].get("activities", [])
        if 0 <= req.activity_index < len(activities):
            activities[req.activity_index] = req.new_activity.model_dump()
            days_plan[req.day_index]["activities"] = activities
            trip_data["days_plan"] = days_plan
            await database.update_trip(trip_id, trip_data)
            return TripResponse(**trip_data)
            
    raise HTTPException(status_code=400, detail="Invalid day or activity index")
