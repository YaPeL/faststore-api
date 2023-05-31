from pydantic import BaseModel

class ProductBase(BaseModel):
    title: str
    sku: str
    images: str
    category: str
    tags: str

class ProductCreate(ProductBase):
    inventory_quantity: int


class ProductResponse(ProductBase):
    id: int
    inventory_quantity: int

    class Config:
        orm_mode = True
