from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    itemss = relationship("CartItem", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    precio = Column(Float)
    codigo = Column(String)
    tipo   = Column(String)


   

################################### orden de compra#########################
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey("productos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="itemss")
    product = relationship("Producto", backref="cart_items")

    @property
    def user_name(self):
        return self.owner.nombre if self.owner else None

    @property
    def product_name(self):
        return self.product.nombre if self.product else None