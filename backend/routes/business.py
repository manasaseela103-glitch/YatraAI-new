from fastapi import APIRouter
from models import BusinessRegister, OfferItem
import database

router = APIRouter(prefix="/business", tags=["Business"])


@router.get("/dashboard")
async def get_dashboard():
    return await database.get_business_data()


@router.post("/register")
async def register(biz: BusinessRegister):
    return await database.register_business(biz.model_dump())


@router.post("/offers")
async def add_offer(offer: OfferItem):
    return await database.add_business_offer(offer.model_dump())
