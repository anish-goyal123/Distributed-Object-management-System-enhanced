from sqlalchemy.orm import Session
from fastapi import HTTPException
from order.models import Order, OrderItem
from product.models import Product
from order.dto import OrderCreate

def process_order(order_req: OrderCreate, user_id: int, db: Session):
    successful_items = []
    failed_items = []

    for batch in order_req.items:
        if len(batch.product_id) != len(batch.quantity):
            raise HTTPException(status_code=400, detail="Product IDs and quantities must match exactly.")

        for pid, qty in zip(batch.product_id, batch.quantity):
            product = db.query(Product).filter(Product.product_id == pid).first()
            
            if not product:
                failed_items.append({"product_id": pid, "reason": "Product does not exist"})
                continue
            if product.product_quantity < qty:
                failed_items.append({"product_id": pid, "reason": f"Insufficient stock. Available: {product.product_quantity}"})
                continue
                
            successful_items.append({"product": product, "qty": qty})

    if not successful_items:
        raise HTTPException(status_code=400, detail={"message": "Order failed.", "failed_items": failed_items})

    new_order = Order(user_id=user_id)
    db.add(new_order)
    db.commit() 
    db.refresh(new_order)

    for item in successful_items:
        product = item["product"]
        qty = item["qty"]
        product.product_quantity -= qty 
        
        order_item = OrderItem(order_id=new_order.id, product_id=product.product_id, quantity=qty)
        db.add(order_item)

    db.commit()

    response = {
        "message": "Order processed successfully." if not failed_items else "Order partially processed.",
        "order_id": new_order.id,
        "items_ordered": [{"product_id": item["product"].product_id, "quantity": item["qty"]} for item in successful_items]
    }
    if failed_items:
        response["failed_items"] = failed_items
    return response

def get_order_details(order_id: int, user_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to view this order.")
    
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return {"order": order, "items": items}