from sqlalchemy.orm import Session
from fastapi import HTTPException
from payment.models import Payment
from payment.dto import PaymentCreate
from order.models import Order

def process_transaction(payment: PaymentCreate, user_id: int, db: Session):
    order = db.query(Order).filter(Order.id == payment.order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only pay for your own orders.")
        
    if order.status == "PAID":
        raise HTTPException(status_code=400, detail="Order is already paid")
    
    new_payment = Payment(order_id=payment.order_id, amount=payment.amount)
    db.add(new_payment)
    
    order.status = "PAID"
    db.commit()
    
    return {"message": "Payment successful", "order_id": order.id, "status": order.status}