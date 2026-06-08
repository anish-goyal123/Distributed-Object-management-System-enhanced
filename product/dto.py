from pydantic import BaseModel
from typing import List

class ProductBatchCreate(BaseModel):
    product_id: List[int]
    product_name: List[str]
    product_quantity: List[int]

class AddStockRequest(BaseModel):
    quantity_to_add: int