import uuid
import datetime
from typing import Dict, Any, List, Optional
import logging
from config import settings

logger = logging.getLogger("yatra.database")

# In-memory database store (acts as robust fallback and mock store)
_memory_store: Dict[str, Any] = {
    "trips": {},
    "users": {},
    "bookings": [],
    "businesses": [
        {
            "id": "biz_1",
            "name": "Heritage Crafts Haveli",
            "category": "Handicrafts & Workshops",
            "location": "Jaipur, Rajasthan",
            "rating": 4.9,
            "description": "Family-run block-printing studio and heritage workshop preserving 200-year-old Rajasthani textile traditions.",
            "contact_email": "info@heritagecrafts.in",
            "phone": "+91 98290 12345",
            "address": "12 Amer Road, Old City, Jaipur"
        }
    ],
    "offers": [
        {"name": "Early Morning Heritage Walk Discount", "discount": "15% off before 10 AM", "validity": "Valid till Dec 2026", "active": True},
        {"name": "Local Family Lunch Package", "discount": "Free dessert platter with thali", "validity": "Ongoing", "active": True},
        {"name": "Block-Printing Souvenir Special", "discount": "Buy 2 scarves get 1 print block", "validity": "Weekends only", "active": True}
    ],
    "leads": [
        {"tourist": "Aarav Sharma", "destination": "Jaipur", "experience": "Old City Morning Walk", "date": "Oct 12, 2026", "status": "Confirmed"},
        {"tourist": "Elena Rostova", "destination": "Jaipur", "experience": "Block Printing Masterclass", "date": "Oct 14, 2026", "status": "Inquiry"},
        {"tourist": "Priya Patel", "destination": "Udaipur", "experience": "Heritage Home Lunch", "date": "Oct 18, 2026", "status": "New Lead"},
        {"tourist": "Marcus Chen", "destination": "Hampi", "experience": "Sunset Boulder Trek", "date": "Oct 21, 2026", "status": "Confirmed"}
    ],
    "sos_alerts": [],
    "destinations": [
        {"name": "Hampi", "region": "Karnataka", "category": "History", "rating": "4.9", "description": "Stone ruins, wild boulders and slow afternoons beside the Tungabhadra.", "budget": "₹18,000", "crowd": "Moderate", "image": "https://images.unsplash.com/photo-1600100397608-f0107f7d5a35?auto=format&fit=crop&w=900&q=85"},
        {"name": "Araku Valley", "region": "Andhra Pradesh", "category": "Nature", "rating": "4.8", "description": "Misty coffee country where mountain trains and forest trails meet.", "budget": "₹14,500", "crowd": "Low", "image": "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=85"},
        {"name": "Jaipur", "region": "Rajasthan", "category": "Popular", "rating": "4.7", "description": "Rose-coloured streets, generous food and a living royal legacy.", "budget": "₹16,000", "crowd": "High", "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=900&q=85"},
        {"name": "Kerala", "region": "Kerala", "category": "Nature", "rating": "4.9", "description": "Backwaters, spice gardens and coastlines made for taking your time.", "budget": "₹22,000", "crowd": "Moderate", "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=900&q=85"},
        {"name": "Meghalaya", "region": "Northeast India", "category": "Adventure", "rating": "4.9", "description": "Living root bridges, cloud forests and rain that makes everything glow.", "budget": "₹24,000", "crowd": "Low", "image": "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=900&q=85"},
        {"name": "Varanasi", "region": "Uttar Pradesh", "category": "Culture", "rating": "4.6", "description": "Ancient ghats, morning light and a city that rewards curiosity.", "budget": "₹12,000", "crowd": "High", "image": "https://images.unsplash.com/photo-1561361058-c24cecae35ca?auto=format&fit=crop&w=900&q=85"},
        {"name": "Udaipur", "region": "Rajasthan", "category": "Popular", "rating": "4.8", "description": "Lakeside mornings, blue hour balconies and unhurried old-world charm.", "budget": "₹17,500", "crowd": "Moderate", "image": "https://images.unsplash.com/photo-1602643163983-ed0babc39797?auto=format&fit=crop&w=900&q=85"},
        {"name": "Goa", "region": "Goa", "category": "Food", "rating": "4.7", "description": "Sunlit villages, small kitchens and a coastline with its own rhythm.", "budget": "₹20,000", "crowd": "High", "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=900&q=85"}
    ],
    "gems": [
        {"place": "Chettinad", "location": "Tamil Nadu", "why": "Mansions, hand-painted tiles and some of South India’s most generous food.", "best": "November – February", "crowd": "Very low", "budget": "₹15,000", "experience": "A heritage home lunch", "tag": "Culture", "image": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=900&q=85"},
        {"place": "Chopta", "location": "Uttarakhand", "why": "A quiet Himalayan meadow with big mountain views and clear night skies.", "best": "March – June", "crowd": "Low", "budget": "₹13,500", "experience": "A guided forest trek", "tag": "Nature", "image": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=900&q=85"},
        {"place": "Majuli", "location": "Assam", "why": "River-island calm, mask-making traditions and a culture unlike anywhere else.", "best": "October – April", "crowd": "Very low", "budget": "₹16,500", "experience": "Meet a mask artisan", "tag": "Culture", "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=85"},
        {"place": "Gurez Valley", "location": "Kashmir", "why": "Wild valleys and warm village stays far from the usual Kashmir circuit.", "best": "May – September", "crowd": "Low", "budget": "₹21,000", "experience": "A night in a wooden homestay", "tag": "Adventure", "image": "https://images.unsplash.com/photo-1486911278844-a81c5267e227?auto=format&fit=crop&w=900&q=85"}
    ],
    "experiences": [
        {"type": "Local Guide", "name": "Old City, New Stories", "provider": "Meera’s Jaipur Walks", "location": "Jaipur, Rajasthan", "rating": "4.9", "price": "₹850 / person", "description": "Follow a local storyteller through lanes, courtyards and family-run workshops.", "image": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=900&q=85"},
        {"type": "Homestay", "name": "The Mango Orchard Stay", "provider": "Anita & family", "location": "Sakleshpur, Karnataka", "rating": "4.8", "price": "₹2,400 / night", "description": "Wake to birdsong, estate coffee and a table set with food from the garden.", "image": "https://images.unsplash.com/photo-1601918774946-25832a4be0d6?auto=format&fit=crop&w=900&q=85"},
        {"type": "Local Restaurant", "name": "A Table at Home", "provider": "Ramesh’s Kitchen", "location": "Kochi, Kerala", "rating": "4.9", "price": "₹1,200 / person", "description": "A warm, intimate meal of recipes passed through three generations.", "image": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=900&q=85"},
        {"type": "Handicrafts", "name": "Clay & Quiet", "provider": "The Potter Collective", "location": "Khurja, Uttar Pradesh", "rating": "4.7", "price": "₹650 / person", "description": "Make something useful with your hands and meet the makers behind the craft.", "image": "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?auto=format&fit=crop&w=900&q=85"},
        {"type": "Cooking Class", "name": "Spice Route Supper", "provider": "Lakshmi’s Table", "location": "Munnar, Kerala", "rating": "5.0", "price": "₹1,500 / person", "description": "Shop, cook and sit down to a fragrant meal in a family kitchen.", "image": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=900&q=85"},
        {"type": "Cultural Workshop", "name": "A Rhythm of Dhol", "provider": "Swarang Studio", "location": "Ahmedabad, Gujarat", "rating": "4.8", "price": "₹900 / person", "description": "Learn the heartbeat of a folk tradition from the artists keeping it alive.", "image": "https://images.unsplash.com/photo-1504609813442-a8924e83f76e?auto=format&fit=crop&w=900&q=85"},
        {"type": "Adventure Activity", "name": "River, Rock, Repeat", "provider": "Wild South Collective", "location": "Dandeli, Karnataka", "rating": "4.9", "price": "₹2,200 / person", "description": "A guided day of river rapids, forest paths and a picnic in the wild.", "image": "https://images.unsplash.com/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&w=900&q=85"}
    ]
}

mongo_client = None
mongo_db = None

async def init_db():
    global mongo_client, mongo_db
    uri = settings.effective_mongodb_uri
    if uri:
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            mongo_client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=2000)
            mongo_db = mongo_client[settings.DATABASE_NAME]
            # Verify connection
            await mongo_client.admin.command('ping')
            logger.info("Connected to MongoDB successfully.")
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}. Falling back to in-memory store.")
            mongo_client = None
            mongo_db = None
    else:
        logger.info("No MongoDB URI configured. Running with in-memory store.")


async def get_db_status() -> Dict[str, Any]:
    if mongo_client is not None and mongo_db is not None:
        try:
            await mongo_client.admin.command('ping')
            return {
                "connected": True,
                "database": settings.DATABASE_NAME,
                "mode": "mongodb"
            }
        except Exception as e:
            return {
                "connected": False,
                "database": settings.DATABASE_NAME,
                "mode": "in-memory-fallback",
                "error": str(e)
            }
    return {
        "connected": False,
        "database": settings.DATABASE_NAME,
        "mode": "in-memory"
    }


async def close_db():
    global mongo_client, mongo_db
    if mongo_client is not None:
        mongo_client.close()
        mongo_client = None
        mongo_db = None


async def save_trip(trip_dict: Dict[str, Any]) -> str:
    trip_id = trip_dict.get("id") or str(uuid.uuid4())[:8]
    trip_dict["id"] = trip_id
    trip_dict["created_at"] = datetime.datetime.utcnow().isoformat()
    
    if mongo_db is not None:
        try:
            await mongo_db.trips.replace_one({"id": trip_id}, trip_dict, upsert=True)
        except Exception as e:
            logger.error(f"Error saving to MongoDB: {e}")
            
    _memory_store["trips"][trip_id] = trip_dict
    return trip_id


async def register_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    user_data["id"] = user_data.get("id") or "usr_" + str(uuid.uuid4())[:8]
    user_data["updated_at"] = datetime.datetime.utcnow().isoformat()
    email = user_data["email"].lower()
    if mongo_db is not None:
        try:
            await mongo_db.users.replace_one({"email": email}, user_data, upsert=True)
        except Exception as e:
            logger.error(f"Error saving user to MongoDB: {e}")
    _memory_store["users"][email] = user_data
    return user_data


async def get_user(email: str) -> Optional[Dict[str, Any]]:
    normalized = email.lower()
    if mongo_db is not None:
        try:
            user = await mongo_db.users.find_one({"email": normalized}, {"_id": 0})
            if user:
                return user
        except Exception as e:
            logger.error(f"Error fetching user from MongoDB: {e}")
    return _memory_store["users"].get(normalized)


async def get_trip(trip_id: str) -> Optional[Dict[str, Any]]:
    if mongo_db is not None:
        try:
            doc = await mongo_db.trips.find_one({"id": trip_id}, {"_id": 0})
            if doc:
                return doc
        except Exception as e:
            logger.error(f"Error fetching from MongoDB: {e}")
            
    return _memory_store["trips"].get(trip_id)


async def update_trip(trip_id: str, updated_data: Dict[str, Any]) -> bool:
    trip = await get_trip(trip_id)
    if not trip:
        return False
    trip.update(updated_data)
    _memory_store["trips"][trip_id] = trip
    if mongo_db is not None:
        try:
            await mongo_db.trips.replace_one({"id": trip_id}, trip, upsert=True)
        except Exception as e:
            logger.error(f"Error updating MongoDB trip: {e}")
    return True


async def get_destinations(category: Optional[str] = None) -> List[Dict[str, Any]]:
    items = _memory_store["destinations"]
    if category and category != "All":
        return [d for d in items if d.get("category") == category]
    return items


async def get_gems(tag: Optional[str] = None, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
    items = _memory_store["gems"]
    if filter_type == "Low Crowd":
        return [g for g in items if "low" in g.get("crowd", "").lower()]
    if filter_type == "Budget Friendly":
        return [g for g in items if int(''.join(filter(str.isdigit, g.get("budget", "0")))) < 16000]
    if tag and tag != "All":
        return [g for g in items if g.get("tag") == tag]
    return items


async def get_experiences(exp_type: Optional[str] = None) -> List[Dict[str, Any]]:
    items = _memory_store["experiences"]
    if exp_type and exp_type != "All":
        return [e for e in items if e.get("type") == exp_type]
    return items


async def create_booking(booking: Dict[str, Any]) -> Dict[str, Any]:
    booking["id"] = "bk_" + str(uuid.uuid4())[:6]
    booking["created_at"] = datetime.datetime.utcnow().isoformat()
    booking["status"] = "Confirmed"
    _memory_store["bookings"].append(booking)
    _memory_store["leads"].insert(0, {
        "tourist": booking.get("tourist_name", "Guest"),
        "destination": booking.get("notes") or "Local Visit",
        "experience": booking.get("experience_name", "Curated Experience"),
        "date": booking.get("date", "Upcoming"),
        "status": "New Booking"
    })
    return booking


async def register_business(business_data: Dict[str, Any]) -> Dict[str, Any]:
    business_data["id"] = "biz_" + str(uuid.uuid4())[:6]
    business_data["created_at"] = datetime.datetime.utcnow().isoformat()
    _memory_store["businesses"].append(business_data)
    return business_data


async def add_business_offer(offer: Dict[str, Any]) -> Dict[str, Any]:
    _memory_store["offers"].insert(0, offer)
    return offer


async def get_business_data() -> Dict[str, Any]:
    active_biz = _memory_store["businesses"][0] if _memory_store["businesses"] else {}
    return {
        "stats": [
            {"label": "Profile views", "value": "1,840", "change": "+18% this month"},
            {"label": "Direct inquiries", "value": "126", "change": "+24% this month"},
            {"label": "Total revenue", "value": "₹1,42,000", "change": "+12% this month"},
            {"label": "Active offers", "value": str(len(_memory_store["offers"])), "change": "3 ongoing promotions"}
        ],
        "profile": active_biz,
        "leads": _memory_store["leads"],
        "experiences": [
            {"name": "Traditional Block Printing Workshop", "price": "₹650", "views": "420", "bookings": "38", "rating": "4.9", "status": "Active"},
            {"name": "Old Haveli Cultural Walking Tour", "price": "₹850", "views": "310", "bookings": "29", "rating": "4.8", "status": "Active"},
            {"name": "Artisan Tea & Textile Storytelling", "price": "₹450", "views": "190", "bookings": "14", "rating": "4.9", "status": "Featured"}
        ],
        "offers": _memory_store["offers"],
        "analytics": [
            {"label": "Direct inquiries", "value": 78},
            {"label": "Profile views", "value": 92},
            {"label": "Booking conversion", "value": 64},
            {"label": "Positive reviews", "value": 96}
        ]
    }


async def log_sos_alert(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    alert_data["id"] = "sos_" + str(uuid.uuid4())[:6]
    alert_data["timestamp"] = datetime.datetime.utcnow().isoformat()
    alert_data["status"] = "Dispatched"
    _memory_store["sos_alerts"].append(alert_data)
    return alert_data


async def get_admin_analytics() -> Dict[str, Any]:
    return {
        "stats": [
            {"label": "Total Visitors Routed", "value": "24,850"},
            {"label": "Hidden Gem Diversion", "value": "38.4%"},
            {"label": "Crowd Pressure Relieved", "value": "42%"},
            {"label": "Local Business Revenue", "value": "₹3.8 Cr"}
        ],
        "tourism_overview": [
            {"label": "Sustainable Tourism Index", "value": 84},
            {"label": "Crowd Balance Efficiency", "value": 76},
            {"label": "Local Economic Retainment", "value": 91},
            {"label": "Traveler Satisfaction", "value": 94}
        ],
        "destinations": [
            {"destination": "Jaipur", "visitors": "8,400", "crowd": "Moderate", "spending": "₹16,200", "trend": "+12%"},
            {"destination": "Hampi", "visitors": "4,150", "crowd": "Low", "spending": "₹18,500", "trend": "+24%"},
            {"destination": "Varanasi", "visitors": "6,800", "crowd": "High", "spending": "₹12,400", "trend": "+8%"},
            {"destination": "Araku Valley", "visitors": "2,300", "crowd": "Low", "spending": "₹14,200", "trend": "+35%"},
            {"destination": "Meghalaya", "visitors": "3,200", "crowd": "Low", "spending": "₹22,800", "trend": "+19%"}
        ],
        "hidden_gem_impact": [
            {"label": "Diverted from Overcrowding", "value": "38.4%"},
            {"label": "Eco-Heritage Preservation", "value": "92%"},
            {"label": "Offbeat Destination Growth", "value": "+44%"}
        ],
        "local_economy": [
            {"label": "Registered Local Guides", "value": "142"},
            {"label": "Artisan Cooperatives", "value": "86"},
            {"label": "Homestays Supported", "value": "210"}
        ],
        "ai_insights": [
            {"title": "Jaipur Peak Footfall Smoothing", "text": "YatraAI recommended early morning Amber Fort entries and evening Kishan Bagh visits, reducing peak hour congestion at City Palace by 26%."},
            {"title": "Hampi Heritage Dispersion", "text": "Dispersed 40% of daytime visitors from Virupaksha Temple to the riverside Anegundi trail, supporting 18 local boatmen and tea stalls."},
            {"title": "Weather Adaptation Trigger", "text": "Recent monsoon squall triggered automated rerouting for 312 travelers to covered havelis and indoor craft ateliers."}
        ]
    }
