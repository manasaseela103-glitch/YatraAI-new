from fastapi import APIRouter
from models import BudgetOptimizeRequest

router = APIRouter(prefix="/budget", tags=["Budget"])


@router.post("/optimize")
async def optimize_budget(req: BudgetOptimizeRequest):
    total = req.budget
    travelers = max(1, req.travelers)
    days = max(1, req.days)
    daily_budget = total / days
    per_person_daily = daily_budget / travelers

    # Categories breakdown
    stay_alloc = total * 0.38
    food_alloc = total * 0.22
    trans_alloc = total * 0.16
    act_alloc = total * 0.24

    # Savings alternatives
    alternatives = [
        {
            "category": "Stay",
            "current": "Upscale Heritage Hotel",
            "alternative": "Verified Local Heritage Homestay / Boutique Haveli",
            "savings": f"₹{round(stay_alloc * 0.30):,}",
            "reason": "Includes authentic home-cooked breakfast and insider local host walking tips."
        },
        {
            "category": "Transit",
            "current": "Chauffeured Private Taxi Everyday",
            "alternative": "E-Auto Rickshaws + Metro Day Pass",
            "savings": f"₹{round(trans_alloc * 0.40):,}",
            "reason": "Navigates narrow historic lanes 2x faster without parking delays."
        },
        {
            "category": "Food",
            "current": "Fine Dining Hotel Restaurants",
            "alternative": "Legendary Heritage Kitchens & Street Food Walk",
            "savings": f"₹{round(food_alloc * 0.35):,}",
            "reason": "Enjoy authentic recipes preserved across generations at half the tariff."
        },
        {
            "category": "Sightseeing",
            "current": "Individual Attraction Entry Counters",
            "alternative": "Smart Tourism Composite Monument E-Pass",
            "savings": f"₹{round(act_alloc * 0.25):,}",
            "reason": "Single digital QR pass valid for all major state monuments and museums."
        }
    ]

    potential_savings = round((stay_alloc * 0.30) + (trans_alloc * 0.40) + (food_alloc * 0.35) + (act_alloc * 0.25))

    return {
        "destination": req.destination,
        "total_budget": total,
        "days": days,
        "travelers": travelers,
        "daily_budget": round(daily_budget, 2),
        "per_person_daily": round(per_person_daily, 2),
        "breakdown": {
            "accommodation": round(stay_alloc, 2),
            "food": round(food_alloc, 2),
            "transport": round(trans_alloc, 2),
            "activities": round(act_alloc, 2),
        },
        "potential_savings": potential_savings,
        "optimized_total": round(total - potential_savings),
        "alternatives": alternatives,
        "smart_tips": [
            f"Pre-book composite monuments pass online to skip ticket queue surcharges in {req.destination}.",
            "Book verified homestays to direct 85% of accommodation spend into local community hands.",
            "Utilize morning e-rickshaws for traffic-free transit between heritage quarters."
        ]
    }
