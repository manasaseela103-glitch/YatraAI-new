from typing import Optional, List
from fastapi import APIRouter, Query
from models import BookingRequest
import database

router = APIRouter(tags=["Discovery"])


@router.get("/destinations")
async def list_destinations(category: Optional[str] = Query("All")):
    return await database.get_destinations(category)


@router.get("/gems")
async def list_hidden_gems(
    tag: Optional[str] = Query("All"),
    filter_type: Optional[str] = Query(None)
):
    return await database.get_gems(tag=tag, filter_type=filter_type)


@router.get("/experiences")
async def list_experiences(type: Optional[str] = Query("All")):
    return await database.get_experiences(exp_type=type)


@router.post("/experiences/book")
async def book_experience(req: BookingRequest):
    return await database.create_booking(req.model_dump())
