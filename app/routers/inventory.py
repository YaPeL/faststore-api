from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends

from app.database import get_db
from app.models import Inventory, Product


router = APIRouter(prefix="/api/v1/inventory",
    tags=["inventory"],
)


@router.get("/{product_id}")
def get_product_inventory(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if product:
        return {"product_id": product.id, "title": product.title, "inventory": product.inventory.quantity}
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.put("/{product_id}/increment/{amount}")
def increment_product_quantity(product_id: int, amount: int, db: Session = Depends(get_db)):
    try:
        with db.begin():
            inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
            if inventory:
                inventory.quantity += amount
                db.commit()
                db.refresh(inventory)
                return {"message": f"Quantity incremented successfully. Current quantity: {inventory}"}
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while incrementing the quantity.")


@router.put("/{product_id}/decrement/{amount}")
def decrement_product_quantity(product_id: int, amount: int, db: Session = Depends(get_db)):
    try:
        with db.begin():
            inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
            if inventory:
                inventory.quantity -= amount
                if inventory.quantity > 0:
                    db.commit()
                    db.refresh(inventory)
                    return {"message": f"Quantity decremented successfully. Current quantity: {inventory}"}
                else:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient inventory")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while decreasing the quantity.")
