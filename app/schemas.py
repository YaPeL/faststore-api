from pydantic import BaseModel
from typing import List, Union


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
    inventory_quantity: int

    class Config:
        orm_mode = True


class ProductInfoSchema(BaseModel):
    title: str
    id: int


class GroupedProductSchema(BaseModel):
    category: Union[str, None]
    tags: Union[str, None]
    products: List[ProductInfoSchema]

