from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from product.models import Product
from product.dto import ProductBatchCreate, AddStockRequest

def create_products(batch: ProductBatchCreate, db: Session):
    if not (len(batch.product_id) == len(batch.product_name) == len(batch.product_quantity)):
        raise HTTPException(status_code=400, detail="The number of IDs, names, and quantities must match exactly.")

    if not batch.product_id:
        raise HTTPException(status_code=400, detail="Must provide at least one product.")

    successful_products = []
    failed_products = []
    seen_ids = set()
    seen_names_lower = set()

    for pid, name, qty in zip(batch.product_id, batch.product_name, batch.product_quantity):
        name_lower = name.lower().strip()

        if pid in seen_ids or name_lower in seen_names_lower:
            failed_products.append({"product_id": pid, "reason": "Duplicate ID or name in request."})
            continue

        if db.query(Product).filter(Product.product_id == pid).first():
            failed_products.append({"product_id": pid, "reason": "Product ID already exists."})
            continue

        if db.query(Product).filter(func.lower(Product.product_name) == name_lower).first():
            failed_products.append({"product_id": pid, "reason": "Product name already exists."})
            continue

        seen_ids.add(pid)
        seen_names_lower.add(name_lower)
        successful_products.append(Product(product_id=pid, product_name=name.strip(), product_quantity=qty))

    if not successful_products:
        raise HTTPException(status_code=400, detail={"message": "Failed to create any products.", "failed_items": failed_products})

    db.add_all(successful_products)
    db.commit()

    response = {
        "message": "Products created successfully." if not failed_products else "Products partially created.",
        "created_products": [{"product_id": p.product_id, "product_name": p.product_name, "quantity": p.product_quantity} for p in successful_products]
    }
    if failed_products:
        response["failed_items"] = failed_products
    return response

def get_all_products(db: Session):
    return db.query(Product).all()

def add_stock(product_id: int, req: AddStockRequest, db: Session):
    if req.quantity_to_add <= 0:
        raise HTTPException(status_code=400, detail="Quantity to add must be greater than zero.")

    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    product.product_quantity += req.quantity_to_add
    db.commit()
    db.refresh(product)
    return {"message": "Stock updated successfully", "updated_product": product}