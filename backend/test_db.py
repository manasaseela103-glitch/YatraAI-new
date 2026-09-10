import asyncio
import sys
import logging
from config import settings
import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_db")

async def test_db_connection():
    print("=" * 50)
    print("Yatra AI - MongoDB Connection & Config Verification")
    print("=" * 50)
    
    print(f"Database Name: {settings.DATABASE_NAME}")
    has_uri = bool(settings.MONGODB_URI)
    has_creds = bool(settings.MONGODB_USERNAME and settings.MONGODB_PASSWORD)
    
    print(f"MONGODB_URI configured: {'Yes' if has_uri else 'No'}")
    print(f"MONGODB Credentials configured: {'Yes' if has_creds else 'No'}")
    
    print("\nInitializing Database connection...")
    await database.init_db()
    
    status = await database.get_db_status()
    print(f"Connection Status: {status}")
    
    if status.get("connected"):
        print("SUCCESS: Connected to MongoDB successfully!")
    else:
        print(f"INFO: Database running in mode '{status.get('mode')}'.")
        
    await database.close_db()
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_db_connection())
