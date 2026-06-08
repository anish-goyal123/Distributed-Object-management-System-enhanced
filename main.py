from fastapi import FastAPI
from database import engine, Base

from auth.controller import router as auth_router
from product.controller import router as product_router
from order.controller import router as order_router
from payment.controller import router as payment_router

# Ensure all models are imported before creating tables
from auth.models import User
from product.models import Product
from order.models import Order, OrderItem
from payment.models import Payment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise E-Commerce Backend")

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(payment_router)

@app.get("/")
def read_root():
    return {"message": "Enterprise E-Commerce API is running securely."}