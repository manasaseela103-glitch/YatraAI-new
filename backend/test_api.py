import sys
import json
import httpx

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    passed = 0
    failed = 0
    
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # Test 1: Root endpoint
        r = client.get("/")
        print("GET / ->", r.status_code, r.json())
        assert r.status_code == 200
        assert r.json().get("status") == "success"
        passed += 1

        # Test 2: Health endpoint
        r = client.get("/api/health")
        print("GET /api/health ->", r.status_code, r.json())
        assert r.status_code == 200
        assert r.json().get("status") == "healthy"
        passed += 1

        # Test 3: Generate trip
        trip_payload = {
            "destination": "Jaipur",
            "dates": "2026-10-15",
            "days": 3,
            "travelers": 2,
            "budget": 35000,
            "style": "Cultural",
            "interests": ["History", "Food", "Culture"]
        }
        r = client.post("/api/trips/generate", json=trip_payload)
        print("POST /api/trips/generate ->", r.status_code)
        assert r.status_code == 200
        trip_data = r.json()
        assert trip_data["destination"] == "Jaipur"
        assert len(trip_data["days_plan"]) == 3
        trip_id = trip_data["id"]
        passed += 1

        # Test 4: Get trip by id
        r = client.get(f"/api/trips/{trip_id}")
        print(f"GET /api/trips/{trip_id} ->", r.status_code)
        assert r.status_code == 200
        passed += 1

        # Test 5: Replan trip
        replan_payload = {
            "trip_id": trip_id,
            "scenario": "Attraction Closed",
            "destination": "Jaipur",
            "days": 3,
            "travelers": 2,
            "budget": 35000,
            "interests": ["History", "Culture"]
        }
        r = client.post("/api/trips/replan", json=replan_payload)
        print("POST /api/trips/replan ->", r.status_code)
        assert r.status_code == 200
        replan_res = r.json()
        assert "alternative" in replan_res
        passed += 1

        # Test 6: Accept replan
        accept_payload = {
            "day_index": 0,
            "activity_index": 0,
            "new_activity": replan_res["new_activity"]
        }
        r = client.put(f"/api/trips/{trip_id}/accept-replan", json=accept_payload)
        print(f"PUT /api/trips/{trip_id}/accept-replan ->", r.status_code)
        assert r.status_code == 200
        updated_trip = r.json()
        assert updated_trip["days_plan"][0]["activities"][0]["place"] == replan_res["alternative"]
        passed += 1

        # Test 7: Destinations
        r = client.get("/api/destinations")
        print("GET /api/destinations ->", r.status_code, len(r.json()), "items")
        assert r.status_code == 200
        assert len(r.json()) > 0
        passed += 1

        # Test 8: Hidden Gems
        r = client.get("/api/gems")
        print("GET /api/gems ->", r.status_code, len(r.json()), "items")
        assert r.status_code == 200
        assert len(r.json()) > 0
        passed += 1

        # Test 9: Experiences & Booking
        r = client.get("/api/experiences")
        print("GET /api/experiences ->", r.status_code, len(r.json()), "items")
        assert r.status_code == 200
        passed += 1

        book_payload = {
            "experience_name": "Old City, New Stories",
            "tourist_name": "Antigravity Tester",
            "email": "tester@yatra.ai",
            "phone": "+91 99999 88888",
            "date": "2026-10-16",
            "travelers": 2,
            "notes": "Testing booking API"
        }
        r = client.post("/api/experiences/book", json=book_payload)
        print("POST /api/experiences/book ->", r.status_code)
        assert r.status_code == 200
        passed += 1

        # Test 10: Budget Optimize
        budget_payload = {
            "destination": "Jaipur",
            "budget": 45000,
            "days": 4,
            "travelers": 2,
            "style": "Cultural"
        }
        r = client.post("/api/budget/optimize", json=budget_payload)
        print("POST /api/budget/optimize ->", r.status_code)
        assert r.status_code == 200
        assert "potential_savings" in r.json()
        passed += 1

        # Test 11: Safety advisories and SOS
        r = client.get("/api/safety/advisories?city=Jaipur")
        print("GET /api/safety/advisories ->", r.status_code)
        assert r.status_code == 200
        assert "emergency_numbers" in r.json()
        passed += 1

        sos_payload = {
            "tourist_name": "Test Traveler",
            "location": "Near Hawa Mahal, Jaipur",
            "lat": 26.9239,
            "lng": 75.8267,
            "emergency_type": "Medical assistance needed",
            "contact_number": "+91 98765 43210"
        }
        r = client.post("/api/safety/sos", json=sos_payload)
        print("POST /api/safety/sos ->", r.status_code)
        assert r.status_code == 200
        assert r.json()["status"] == "EMERGENCY_DISPATCHED"
        passed += 1

        # Test 12: Business Dashboard & Register
        r = client.get("/api/business/dashboard")
        print("GET /api/business/dashboard ->", r.status_code)
        assert r.status_code == 200
        passed += 1

        biz_payload = {
            "name": "Amber Folk Pottery Studio",
            "category": "Handicrafts",
            "location": "Amber Village, Jaipur",
            "rating": 4.9,
            "description": "Terracotta and blue pottery handcrafted by rural village artisans.",
            "contact_email": "amberpottery@yatra.ai",
            "phone": "+91 98290 55555",
            "address": "45 Temple Road, Amber"
        }
        r = client.post("/api/business/register", json=biz_payload)
        print("POST /api/business/register ->", r.status_code)
        assert r.status_code == 200
        passed += 1

        # Test 13: Admin Analytics
        r = client.get("/api/admin/analytics")
        print("GET /api/admin/analytics ->", r.status_code)
        assert r.status_code == 200
        assert "tourism_overview" in r.json()
        passed += 1

    print(f"\nAll {passed} backend API tests PASSED successfully! (0 failed)")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
