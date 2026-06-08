from pydantic import BaseModel
from typing import List

class OrderBatchSchema(BaseModel):
    product_id: List[int]
    quantity: List[int]

class OrderCreate(BaseModel):
    items: List[OrderBatchSchema]