from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth.dto import AuthRequest
from auth import service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(req: AuthRequest, db: Session = Depends(get_db)):
    return service.register_user(req, db)

@router.post("/login")
def login(req: AuthRequest, db: Session = Depends(get_db)):
    return service.login_user(req, db)