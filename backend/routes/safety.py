from typing import Optional
from fastapi import APIRouter
from models import SOSAlert
import database

router = APIRouter(prefix="/safety", tags=["Safety"])


@router.get("/advisories")
async def get_safety_advisories(city: Optional[str] = "Jaipur"):
    return {
        "city": city,
        "safety_index": "94% Safe",
        "emergency_numbers": [
            {"service": "National All-in-One Emergency", "number": "112", "type": "Toll Free (24/7)"},
            {"service": "Tourist Police Helpline", "number": "1363", "type": "Multi-lingual Tourist Help"},
            {"service": "Police Control Room", "number": "100", "type": "Police Emergency"},
            {"service": "Ambulance & Medical Emergency", "number": "108", "type": "Medical Dispatch"},
            {"service": "Women Safety Helpline", "number": "1091", "type": "24/7 Dedicated Support"}
        ],
        "safe_zones": [
            {"area": "Old Walled City Heritage Zone", "status": "Highly Patrolled", "note": "Well-lit pedestrian avenues with active tourist assistance booths every 500m."},
            {"area": "Civil Lines & Central Plaza", "status": "24/7 Safe Zone", "note": "High police presence, hospital clusters, and continuous public transit."},
            {"area": "Amer Fort Footpath & Promenade", "status": "Recommended Daytime / Early Evening", "note": "Safe until 8:30 PM with state tourism marshals on duty."}
        ],
        "emergency_hubs": [
            {"name": "SMS Government Multi-Specialty Hospital", "contact": "+91 141 251 8200", "distance": "2.4 km", "type": "Medical"},
            {"name": "Tourist Police Assistance Post (Hawa Mahal)", "contact": "+91 141 260 1002", "distance": "0.8 km", "type": "Police"},
            {"name": "Fortis Escorts Emergency Center", "contact": "+91 141 254 7000", "distance": "5.1 km", "type": "Medical"}
        ],
        "safety_protocols": [
            "Always verify registered tourist cab QR codes before boarding.",
            "Use well-illuminated main bazaar corridors when strolling after 9:30 PM.",
            "Keep emergency offline map cache downloaded on your mobile device."
        ]
    }


@router.post("/sos")
async def trigger_sos(alert: SOSAlert):
    result = await database.log_sos_alert(alert.model_dump())
    return {
        "status": "EMERGENCY_DISPATCHED",
        "alert_id": result.get("id"),
        "timestamp": result.get("timestamp"),
        "message": f"SOS Alert active for {alert.tourist_name} at {alert.location}. Nearest Tourist Police & Medical units notified.",
        "emergency_hotline": "112",
        "tourist_helpline": "1363",
        "nearest_station": "Central Tourist Police Control Room",
        "action_advice": "Stay in a well-lit, public location if safe to do so. Help is on the way."
    }
