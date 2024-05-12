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

    class Config:
        orm_mode = True



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

class Compra(BaseModel):
    id: int
    owner_id: int | None = None
    product_id: int | None = None
    class Config:
        orm_mode = True


class CompraBase(BaseModel):
    owner_id: int
    product_id: int

    class Config:
        orm_mode = True

class Compra(CompraBase):
    id: int
    owner: Optional[UserBase]

    class Config:
        orm_mode = True

