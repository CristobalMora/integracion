from pydantic import BaseModel
from typing import List, Optional


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    title: str
    description: str | None = None
    owner_id: int | None = None

    class Config:
        orm_mode = True

class ItemUpdate(ItemBase):
    pass

############################################ user #####################################

class UserBase(BaseModel):
    email: str
    nombre: str
    

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int

class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

######################################### producto #######################

class Producto(BaseModel):
    
    nombre: str
    precio: float
    codigo: str
    tipo  : str

class ProductoId(Producto):
    id: int

    class Config:
        orm_mode = True

############################################ orden de compra  #############################

class CartItemBase(BaseModel):
    quantity: int

class CartItemCreate(CartItemBase):
    product_id: int
    user_id: int

class CartItem(CartItemBase):
    id: int
    product: Producto
    user: User

    class Config:
        orm_mode = True