from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from auth.models import User
from order.dto import OrderCreate
from order import service

router = APIRouter(prefix="/orders", tags=["Order"])

@router.post("/") 
def create(order_req: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.process_order(order_req, current_user.id, db)

@router.get("/{order_id}") 
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_order_details(order_id, current_user.id, db)