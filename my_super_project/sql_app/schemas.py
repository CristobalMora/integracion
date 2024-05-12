from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class ItemUpdate(ItemBase):
    pass

############################################ user #####################################

class UserBase(BaseModel):
    email: str
    nombre:str


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

######################################### producto#######################
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    codigo: str

    class Config:
        orm_mode = True