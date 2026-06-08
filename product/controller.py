from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from auth.models import User
from product.dto import ProductBatchCreate, AddStockRequest
from product import service

router = APIRouter(prefix="/products", tags=["Product"])

@router.post("/") 
def create(batch: ProductBatchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.create_products(batch, db)

@router.get("/") 
def get_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_all_products(db)

@router.patch("/{product_id}/add-stock") 
def add_stock(product_id: int, req: AddStockRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.add_stock(product_id, req, db)