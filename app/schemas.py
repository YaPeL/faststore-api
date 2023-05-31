from pydantic import BaseModel

class ProductBase(BaseModel):
    title: str
    sku: str
    images: str
    category: str
    tags: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
