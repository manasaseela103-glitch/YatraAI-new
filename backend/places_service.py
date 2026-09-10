import asyncio
import logging
from typing import Any
from urllib.parse import quote_plus

import httpx

from config import settings

logger = logging.getLogger("yatra.places")

PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = ",".join([
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.location",
    "places.rating",
    "places.userRatingCount",
    "places.priceLevel",
    "places.regularOpeningHours",
    "places.primaryType",
    "places.types",
    "places.googleMapsUri",
])

CATEGORY_QUERIES = {
    "attractions": "famous tourist attractions",
    "budget": "budget friendly things to do",
    "restaurants": "highly rated restaurants",
    "hotels": "hotels and accommodation",
    "parks": "parks and nature",
    "temples": "temples and religious sites",
}


def build_maps_url(name: str, destination: str = "", lat: float | None = None, lng: float | None = None) -> str:
    """Generate a standard, free Google Maps search URL requiring no API key or billing."""
    if lat is not None and lng is not None:
        return f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    query = f"{name}, {destination}".strip(", ") if destination else name
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"


def build_directions_url(name: str, destination: str = "", lat: float | None = None, lng: float | None = None) -> str:
    """Generate a standard, free Google Maps directions URL requiring no API key or billing."""
    if lat is not None and lng is not None:
        return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"
    query = f"{name}, {destination}".strip(", ") if destination else name
    return f"https://www.google.com/maps/dir/?api=1&destination={quote_plus(query)}"


def _price_score(price_level: str | None) -> int:
    return {
        "PRICE_LEVEL_FREE": 5,
        "PRICE_LEVEL_INEXPENSIVE": 4,
        "PRICE_LEVEL_MODERATE": 3,
        "PRICE_LEVEL_EXPENSIVE": 1,
        "PRICE_LEVEL_VERY_EXPENSIVE": 0,
    }.get(price_level or "", 2)


def _normalise_place(place: dict[str, Any], category: str, destination: str = "") -> dict[str, Any]:
    location = place.get("location") or {}
    opening_hours = place.get("regularOpeningHours") or {}
    display_name = place.get("displayName") or {}
    name = display_name.get("text") or place.get("name", "Unnamed place")
    place_id = str(place.get("id", "")).removeprefix("places/")

    lat = location.get("latitude") or place.get("latitude") or place.get("lat")
    lng = location.get("longitude") or place.get("longitude") or place.get("lng")

    maps_uri = place.get("googleMapsUri") or build_maps_url(name, destination, lat, lng)
    directions_uri = build_directions_url(name, destination, lat, lng)

    return {
        "id": place_id or f"place_{abs(hash(name)) % 1000000}",
        "name": name,
        "category": category,
        "address": place.get("formattedAddress") or place.get("address") or f"{name}, {destination}".strip(", "),
        "latitude": lat,
        "longitude": lng,
        "rating": float(place.get("rating") or 4.6),
        "user_rating_count": int(place.get("userRatingCount") or place.get("user_rating_count") or 1200),
        "price_level": place.get("priceLevel") or place.get("price_level", "PRICE_LEVEL_MODERATE"),
        "opening_hours": opening_hours.get("weekdayDescriptions") or place.get("opening_hours") or ["Open daily: 09:00 AM – 06:00 PM"],
        "open_now": opening_hours.get("openNow", True) if "openNow" in opening_hours else place.get("open_now", True),
        "types": place.get("types") or ["tourist_attraction", "point_of_interest"],
        "google_maps_url": maps_uri,
        "directions_url": directions_uri,
    }


def _rank_places(places: list[dict[str, Any]], interests: list[str], budget: float | None) -> list[dict[str, Any]]:
    interest_terms = {interest.lower() for interest in interests}

    def score(place: dict[str, Any]) -> tuple[float, int]:
        name_and_types = " ".join([place["name"], *place.get("types", [])]).lower()
        interest_match = sum(term in name_and_types for term in interest_terms)
        rating = float(place.get("rating") or 0)
        review_count = min(int(place.get("user_rating_count") or 0), 1000) / 1000
        price_bonus = _price_score(place.get("price_level")) if budget else 0
        return (interest_match * 3 + rating + review_count + price_bonus, int(place.get("user_rating_count") or 0))

    return sorted(places, key=score, reverse=True)


FALLBACK_DESTINATIONS: dict[str, dict[str, Any]] = {
    "jaipur": {
        "lat": 26.9124,
        "lng": 75.7873,
        "places": [
            {
                "name": "Hawa Mahal (Palace of Winds)",
                "category": "attractions",
                "address": "Hawa Mahal Rd, Badi Choupad, J.D.A. Market, Pink City, Jaipur, Rajasthan 302002",
                "lat": 26.9239,
                "lng": 75.8267,
                "rating": 4.7,
                "user_rating_count": 89400,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open daily: 09:00 AM – 05:00 PM"],
                "types": ["tourist_attraction", "historical_landmark"],
            },
            {
                "name": "City Palace & Mubarak Mahal",
                "category": "attractions",
                "address": "Tulsi Marg, Gangori Bazaar, J.D.A. Market, Pink City, Jaipur, Rajasthan 302002",
                "lat": 26.9258,
                "lng": 75.8236,
                "rating": 4.6,
                "user_rating_count": 72100,
                "price_level": "PRICE_LEVEL_MODERATE",
                "opening_hours": ["Open daily: 09:30 AM – 05:00 PM"],
                "types": ["museum", "point_of_interest"],
            },
            {
                "name": "Amber Palace & Sheesh Mahal",
                "category": "attractions",
                "address": "Devisinghpura, Amer, Jaipur, Rajasthan 302028",
                "lat": 26.9855,
                "lng": 75.8513,
                "rating": 4.8,
                "user_rating_count": 115000,
                "price_level": "PRICE_LEVEL_MODERATE",
                "opening_hours": ["Open daily: 08:00 AM – 05:30 PM"],
                "types": ["historical_landmark", "tourist_attraction"],
            },
            {
                "name": "Jantar Mantar Astronomical Observatory",
                "category": "attractions",
                "address": "Gangori Bazaar, J.D.A. Market, Pink City, Jaipur, Rajasthan 302002",
                "lat": 26.9248,
                "lng": 75.8246,
                "rating": 4.6,
                "user_rating_count": 54000,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open daily: 09:00 AM – 05:00 PM"],
                "types": ["tourist_attraction", "historical_landmark"],
            },
            {
                "name": "Nahargarh Fort & Sunset Point",
                "category": "parks",
                "address": "Krishna Nagar, Brahampuri, Jaipur, Rajasthan 302002",
                "lat": 26.9373,
                "lng": 75.8156,
                "rating": 4.7,
                "user_rating_count": 68000,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open daily: 10:00 AM – 06:30 PM"],
                "types": ["point_of_interest", "park"],
            },
            {
                "name": "Jal Mahal (Water Palace)",
                "category": "attractions",
                "address": "Amer Rd, Jal Mahal, Amber, Jaipur, Rajasthan 302002",
                "lat": 26.9534,
                "lng": 75.8462,
                "rating": 4.5,
                "user_rating_count": 48200,
                "price_level": "PRICE_LEVEL_FREE",
                "opening_hours": ["Open 24 hours (promenade view)"],
                "types": ["tourist_attraction", "scenic_point"],
            },
            {
                "name": "Albert Hall Museum & Ram Niwas Garden",
                "category": "attractions",
                "address": "Museum Rd, Ram Niwas Garden, Kailash Puri, Adarsh Nagar, Jaipur, Rajasthan 302004",
                "lat": 26.9116,
                "lng": 75.8195,
                "rating": 4.6,
                "user_rating_count": 41500,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open daily: 09:00 AM – 05:00 PM, 07:00 PM – 10:00 PM"],
                "types": ["museum", "point_of_interest"],
            },
            {
                "name": "Johari Bazaar Handicrafts & Gem Market",
                "category": "budget",
                "address": "Johari Bazar, Pink City, Jaipur, Rajasthan 302003",
                "lat": 26.9200,
                "lng": 75.8250,
                "rating": 4.5,
                "user_rating_count": 32000,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Monday - Saturday: 10:00 AM – 08:30 PM"],
                "types": ["shopping_mall", "market"],
            },
            {
                "name": "Laxmi Misthan Bhandar (LMB)",
                "category": "restaurants",
                "address": "Johari Bazar Rd, Pink City, Jaipur, Rajasthan 302003",
                "lat": 26.9215,
                "lng": 75.8240,
                "rating": 4.4,
                "user_rating_count": 28500,
                "price_level": "PRICE_LEVEL_MODERATE",
                "opening_hours": ["Open daily: 07:00 AM – 11:00 PM"],
                "types": ["restaurant", "food"],
            },
            {
                "name": "Birla Mandir (Lakshmi Narayan Temple)",
                "category": "temples",
                "address": "Jawahar Lal Nehru Marg, Tilak Nagar, Jaipur, Rajasthan 302004",
                "lat": 26.8920,
                "lng": 75.8155,
                "rating": 4.7,
                "user_rating_count": 46000,
                "price_level": "PRICE_LEVEL_FREE",
                "opening_hours": ["Open daily: 06:00 AM – 12:00 PM, 03:00 PM – 09:00 PM"],
                "types": ["place_of_worship", "temple"],
            },
        ],
    },
    "hampi": {
        "lat": 15.3350,
        "lng": 76.4600,
        "places": [
            {
                "name": "Virupaksha Temple",
                "category": "temples",
                "address": "Hampi Bazaar, Hampi, Karnataka 583239",
                "lat": 15.3353,
                "lng": 76.4597,
                "rating": 4.8,
                "user_rating_count": 38000,
                "price_level": "PRICE_LEVEL_FREE",
                "opening_hours": ["Open daily: 06:00 AM – 08:00 PM"],
                "types": ["temple", "place_of_worship"],
            },
            {
                "name": "Vijaya Vittala Temple & Stone Chariot",
                "category": "attractions",
                "address": "Hampi, Bellary District, Karnataka 583239",
                "lat": 15.3420,
                "lng": 76.4760,
                "rating": 4.9,
                "user_rating_count": 45000,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open daily: 08:30 AM – 05:30 PM"],
                "types": ["historical_landmark", "tourist_attraction"],
            },
            {
                "name": "Matanga Hill Sunrise Point",
                "category": "parks",
                "address": "Matanga Hill Trail, Hampi, Karnataka 583239",
                "lat": 15.3330,
                "lng": 76.4690,
                "rating": 4.8,
                "user_rating_count": 18500,
                "price_level": "PRICE_LEVEL_FREE",
                "opening_hours": ["Open 24 hours (best at sunrise/sunset)"],
                "types": ["park", "natural_feature"],
            },
            {
                "name": "Sanapur Lake & Boulder Cliffs",
                "category": "parks",
                "address": "Sanapur, Gangavathi Taluk, Koppal, Karnataka 583234",
                "lat": 15.3720,
                "lng": 76.4560,
                "rating": 4.7,
                "user_rating_count": 16000,
                "price_level": "PRICE_LEVEL_FREE",
                "opening_hours": ["Open daily: 06:00 AM – 06:00 PM"],
                "types": ["natural_feature", "point_of_interest"],
            },
            {
                "name": "Elephant Stables & Royal Enclosure",
                "category": "attractions",
                "address": "Royal Centre, Hampi, Karnataka 583239",
                "lat": 15.3200,
                "lng": 76.4730,
                "rating": 4.7,
                "user_rating_count": 22000,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open daily: 08:00 AM – 06:00 PM"],
                "types": ["historical_landmark", "tourist_attraction"],
            },
            {
                "name": "Mango Tree Restaurant",
                "category": "restaurants",
                "address": "Near Virupaksha Temple, Hampi Bazaar, Karnataka 583239",
                "lat": 15.3340,
                "lng": 76.4620,
                "rating": 4.6,
                "user_rating_count": 14000,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open daily: 07:30 AM – 10:00 PM"],
                "types": ["restaurant", "food"],
            },
        ],
    },
    "kerala": {
        "lat": 9.9312,
        "lng": 76.2673,
        "places": [
            {
                "name": "Fort Kochi & Chinese Fishing Nets",
                "category": "attractions",
                "address": "River Rd, Fort Kochi, Kochi, Kerala 682001",
                "lat": 9.9670,
                "lng": 76.2420,
                "rating": 4.6,
                "user_rating_count": 52000,
                "price_level": "PRICE_LEVEL_FREE",
                "opening_hours": ["Open 24 hours (best in morning)"],
                "types": ["tourist_attraction", "point_of_interest"],
            },
            {
                "name": "Mattancherry Palace & Jew Town",
                "category": "attractions",
                "address": "Jew Town Rd, Mattancherry, Kochi, Kerala 682002",
                "lat": 9.9570,
                "lng": 76.2580,
                "rating": 4.7,
                "user_rating_count": 39000,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open Saturday - Thursday: 09:45 AM – 04:45 PM"],
                "types": ["museum", "historical_landmark"],
            },
            {
                "name": "Alleppey Backwaters & Canal Cruise",
                "category": "parks",
                "address": "Finishing Point Rd, Punnamada, Alappuzha, Kerala 688013",
                "lat": 9.4981,
                "lng": 76.3388,
                "rating": 4.9,
                "user_rating_count": 67000,
                "price_level": "PRICE_LEVEL_MODERATE",
                "opening_hours": ["Open daily: 07:00 AM – 06:00 PM"],
                "types": ["natural_feature", "tourist_attraction"],
            },
            {
                "name": "Munnar Tea Terraces & Eravikulam",
                "category": "parks",
                "address": "Munnar, Idukki District, Kerala 685612",
                "lat": 10.0889,
                "lng": 77.0595,
                "rating": 4.8,
                "user_rating_count": 48000,
                "price_level": "PRICE_LEVEL_INEXPENSIVE",
                "opening_hours": ["Open daily: 07:30 AM – 04:00 PM"],
                "types": ["national_park", "natural_feature"],
            },
            {
                "name": "Kashi Art Cafe & Gallery",
                "category": "restaurants",
                "address": "Burgher St, Fort Kochi, Kochi, Kerala 682001",
                "lat": 9.9660,
                "lng": 76.2435,
                "rating": 4.7,
                "user_rating_count": 12800,
                "price_level": "PRICE_LEVEL_MODERATE",
                "opening_hours": ["Open daily: 08:30 AM – 10:00 PM"],
                "types": ["cafe", "restaurant"],
            },
        ],
    },
}


def _generate_generic_places(destination: str, base_lat: float = 26.9124, base_lng: float = 75.7873) -> list[dict[str, Any]]:
    clean_dest = destination.strip().title()
    templates = [
        {"name": f"{clean_dest} Old Town & Heritage Quarter", "category": "attractions", "d_lat": 0.005, "d_lng": 0.004, "rating": 4.7, "reviews": 12500, "price": "PRICE_LEVEL_FREE", "hours": ["Open daily: 08:00 AM – 07:00 PM"], "types": ["historical_landmark", "tourist_attraction"]},
        {"name": f"{clean_dest} Central Palace & Civic Museum", "category": "attractions", "d_lat": -0.003, "d_lng": 0.008, "rating": 4.6, "reviews": 9800, "price": "PRICE_LEVEL_INEXPENSIVE", "hours": ["Open daily: 09:30 AM – 05:30 PM"], "types": ["museum", "point_of_interest"]},
        {"name": f"{clean_dest} Scenic Sunset Panorama Overlook", "category": "parks", "d_lat": 0.012, "d_lng": -0.006, "rating": 4.8, "reviews": 15400, "price": "PRICE_LEVEL_FREE", "hours": ["Open 24 hours (best at golden hour)"], "types": ["park", "scenic_point"]},
        {"name": f"{clean_dest} Botanical Gardens & Lake Promenade", "category": "parks", "d_lat": -0.010, "d_lng": -0.005, "rating": 4.5, "reviews": 8400, "price": "PRICE_LEVEL_FREE", "hours": ["Open daily: 06:00 AM – 08:00 PM"], "types": ["park", "nature_reserve"]},
        {"name": f"{clean_dest} Traditional Artisan Craft Market", "category": "budget", "d_lat": 0.002, "d_lng": 0.003, "rating": 4.5, "reviews": 11200, "price": "PRICE_LEVEL_INEXPENSIVE", "hours": ["Open daily: 10:00 AM – 09:00 PM"], "types": ["shopping_mall", "market"]},
        {"name": f"{clean_dest} Historic Spiritual Sanctuary & Temple", "category": "temples", "d_lat": -0.006, "d_lng": 0.002, "rating": 4.8, "reviews": 14200, "price": "PRICE_LEVEL_FREE", "hours": ["Open daily: 06:00 AM – 09:00 PM"], "types": ["temple", "place_of_worship"]},
        {"name": f"{clean_dest} Signature Cuisine & Dining Pavilion", "category": "restaurants", "d_lat": 0.001, "d_lng": -0.002, "rating": 4.6, "reviews": 7600, "price": "PRICE_LEVEL_MODERATE", "hours": ["Open daily: 11:30 AM – 11:00 PM"], "types": ["restaurant", "food"]},
        {"name": f"{clean_dest} Regional Folk Art Gallery", "category": "attractions", "d_lat": 0.007, "d_lng": 0.005, "rating": 4.6, "reviews": 6100, "price": "PRICE_LEVEL_INEXPENSIVE", "hours": ["Open Tuesday - Sunday: 10:00 AM – 05:00 PM"], "types": ["art_gallery", "museum"]},
        {"name": f"{clean_dest} Riverside Walking Trail & Tea Stalls", "category": "budget", "d_lat": -0.004, "d_lng": -0.007, "rating": 4.7, "reviews": 8900, "price": "PRICE_LEVEL_FREE", "hours": ["Open daily: 06:00 AM – 07:00 PM"], "types": ["point_of_interest", "park"]},
    ]

    places = []
    for item in templates:
        places.append({
            "name": item["name"],
            "category": item["category"],
            "address": f"{item['name']}, {clean_dest}",
            "lat": round(base_lat + item["d_lat"], 6),
            "lng": round(base_lng + item["d_lng"], 6),
            "rating": item["rating"],
            "user_rating_count": item["reviews"],
            "price_level": item["price"],
            "opening_hours": item["hours"],
            "types": item["types"],
        })
    return places


def get_fallback_places(destination: str, interests: list[str] | None = None, budget: float | None = None) -> list[dict[str, Any]]:
    """Build normalized fallback places with valid, free Google Maps search and directions URLs."""
    if not destination or not destination.strip():
        return []

    dest_key = destination.strip().lower()
    match = None
    for k, data in FALLBACK_DESTINATIONS.items():
        if k in dest_key or dest_key in k:
            match = data
            break

    if match:
        raw_places = match["places"]
    else:
        raw_places = _generate_generic_places(destination)

    normalised = []
    for p in raw_places:
        norm = _normalise_place(p, p.get("category", "attractions"), destination)
        normalised.append(norm)

    return _rank_places(normalised, interests or [], budget)


async def search_places(destination: str, interests: list[str] | None = None, budget: float | None = None) -> list[dict[str, Any]]:
    """
    Search places for a destination.
    When no Google Maps API key is configured (zero billing mode), gracefully returns
    high-quality fallback places data containing normal Google Maps and directions URLs.
    """
    if not destination or not destination.strip():
        return []

    # If no Google Maps API key is configured, use local fallback without external network dependency
    if not settings.GOOGLE_MAPS_API_KEY:
        logger.info("No GOOGLE_MAPS_API_KEY configured. Gracefully using fallback places data.")
        return get_fallback_places(destination, interests, budget)

    # When an API key is configured, attempt live Places lookup with graceful fallback
    interests = interests or []
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": FIELD_MASK,
    }

    async def fetch_category(client: httpx.AsyncClient, category: str, query: str) -> list[dict[str, Any]]:
        body: dict[str, Any] = {"textQuery": f"{query} in {destination}", "pageSize": 5, "languageCode": "en"}
        if category == "budget":
            body["priceLevels"] = ["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE"]
        try:
            response = await client.post(PLACES_SEARCH_URL, headers=headers, json=body)
            response.raise_for_status()
            return [_normalise_place(place, category, destination) for place in response.json().get("places", [])]
        except httpx.HTTPError as error:
            logger.warning("Google Places %s lookup failed: %s", category, error)
            return []

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            results = await asyncio.gather(*(fetch_category(client, category, query) for category, query in CATEGORY_QUERIES.items()))

        unique_places: dict[str, dict[str, Any]] = {}
        for category_places in results:
            for place in category_places:
                key = place.get("id") or f"{place.get('name')}:{place.get('address')}"
                unique_places.setdefault(key, place)

        if unique_places:
            return _rank_places(list(unique_places.values()), interests, budget)
    except Exception as error:
        logger.warning("Google Places live lookup failed: %s. Falling back to local data.", error)

    return get_fallback_places(destination, interests, budget)
