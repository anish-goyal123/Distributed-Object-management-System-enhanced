from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from auth.models import User
from payment.dto import PaymentCreate
from payment import service

router = APIRouter(prefix="/payments", tags=["Payment"])

@router.post("/") 
def process(payment: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.process_transaction(payment, current_user.id, db)