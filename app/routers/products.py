from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Inventory
from app.schemas import ProductResponse, ProductCreate

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


@router.get("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product_schema = ProductResponse.from_orm(product)
    serialized_product = product_schema.dict()
    return serialized_product


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}


@router.get("/")
async def get_products(sort_by: str = None, db: Session = Depends(get_db)):
    if sort_by == "title":
        products = db.query(Product).order_by(Product.title).all()
    elif sort_by == "date_created":
        products = db.query(Product).order_by(Product.id).all()
    else:
        products = db.query(Product).all()
    return products


@router.post("/")
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):

    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    inventory = Inventory(product_id=db_product.id, quantity=1)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    product_schema = ProductResponse.from_orm(db_product)
    serialized_product = product_schema.dict()
    return serialized_product


@router.get("/group")
async def group_products(group_by: str, db: Session = Depends(get_db)):
    if group_by == "category":
        grouped_products = db.query(Product.category).distinct().all()
    elif group_by == "tags":
        grouped_products = db.query(Product.tags).distinct().all()
    else:
        return {"message": "Invalid group_by parameter"}
    return grouped_products
