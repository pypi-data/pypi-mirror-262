# models.py

from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    title: str
    price: str
    discount: Optional[str]
    link: str
    price_no_discount: str
    image_url: str

class ScrapeResult(BaseModel):
    total_pages: str
    views: str
    products: List[Product]

    
class Banner(BaseModel):
    link: str
    image_url: str
    alt_text: str
    title: str
