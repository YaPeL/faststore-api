from enum import Enum
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Product, Inventory
from app.schemas import ProductResponse, ProductCreate, GroupedProductSchema


router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


class GroupBy(str, Enum):
    category = "category"
    tags = "tags"


class SortBy(str, Enum):
    title = "title"
    created_at = "created_at"


class OrderBy(str, Enum):
    asc = "asc"
    desc = "desc"


@router.post("/", response_model=ProductResponse)
async def add_product(product: ProductCreate,
                      db: Session = Depends(get_db)):

    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    inventory = Inventory(product_id=db_product.id, quantity=1)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return db_product


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}


@router.get("/", response_model=List[ProductResponse])
async def get_products(sort_by: SortBy = Query(..., description="Grouping type"),
                       order_by: OrderBy = Query(..., description="Sorting type"),
                       db: Session = Depends(get_db)):
    if sort_by == SortBy.title:
        if order_by == OrderBy.desc:
            products = db.query(Product).order_by(Product.title.desc())
        else:
            products = db.query(Product).order_by(Product.title.asc())
    elif sort_by == SortBy.created_at:
        if order_by == OrderBy.desc:
            products = db.query(Product).order_by(Product.created_at.desc())
        else:
            products = db.query(Product).order_by(Product.created_at.asc())
    else:
        return {"message": "Invalid group_by parameter"}
    return products.all()


@router.get("/group", response_model=List[GroupedProductSchema])
async def group_products(group_by: GroupBy = Query(..., description="Grouping type"),
                         order_by: OrderBy = Query(..., description="Sorting type"),
                         db: Session = Depends(get_db)):
    if group_by == GroupBy.category:
        if order_by == OrderBy.desc:
            grouped_products = db.query(Product.category,
                                        func.json_agg(func.json_build_object('title', Product.title,
                                                                             'id', Product.id))
                                        .label('products')).group_by(Product.category).order_by(Product.category.desc())
        else:
            grouped_products = db.query(Product.category,
                                        func.json_agg(func.json_build_object('title', Product.title,
                                                                             'id', Product.id))
                                        .label('products')).group_by(Product.category).order_by(Product.category.asc())
    elif group_by == GroupBy.tags:
        if order_by == OrderBy.desc:
            grouped_products = db.query(Product.tags,
                                        func.json_agg(func.json_build_object('title', Product.title,
                                                                             'id', Product.id))
                                        .label('products')).group_by(Product.tags).order_by(Product.tags.desc())
        else:
            grouped_products = db.query(Product.tags,
                                        func.json_agg(func.json_build_object('title', Product.title,
                                                                             'id', Product.id))
                                        .label('products')).group_by(Product.tags).order_by(Product.tags.asc())
    else:
        return {"message": "Invalid group_by parameter"}
    return grouped_products.all()
