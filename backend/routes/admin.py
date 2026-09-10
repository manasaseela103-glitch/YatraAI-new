from fastapi import APIRouter
import database

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/analytics")
async def get_analytics():
    return await database.get_admin_analytics()
