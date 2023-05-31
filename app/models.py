import databases
import datetime
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    ForeignKey
)
from app.config import Config

config = Config()
DATABASE_URL = config.get("SQLALCHEMY_DATABASE_URL")
database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    sku = Column(String, index=True)
    images = Column(Text)
    category = Column(String, index=True)
    tags = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    inventory = relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete")

    @property
    def inventory_quantity(self):
        return self.inventory.quantity if self.inventory else 0

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)
    product = relationship("Product", back_populates="inventory", uselist=False)


engine = sqlalchemy.create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
