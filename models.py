from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 商品マスタ関連のモデル
class ProductInfo(BaseModel):
    prd_id: int
    code: str
    name: str
    price: int

class ProductSearchRequest(BaseModel):
    code: str

class ProductSearchResponse(BaseModel):
    product_info: Optional[ProductInfo] = None
    message: Optional[str] = None

# 購入関連のモデル
class PurchaseItem(BaseModel):
    prd_id: int
    code: str
    name: str
    price: int

class PurchaseRequest(BaseModel):
    emp_cd: str = "9999999999"
    store_cd: str = "30"
    pos_no: str = "90"
    items: List[PurchaseItem]

class PurchaseResponse(BaseModel):
    success: bool
    total_amount: int
    message: Optional[str] = None
