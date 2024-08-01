import datetime
from pydantic import BaseModel, Field, EmailStr

current_datetime = datetime.datetime.now()


class UserIn(BaseModel):
    firstname: str = Field(..., title="Firstname", max_length=50)
    lastname: str = Field(..., title="Lastname", max_length=50)
    email: EmailStr = Field(..., title="Email", max_length=128)
    password: str = Field(..., title="Password", min_length=4)


class User(BaseModel):
    id_user: int
    firstname: str = Field(..., title="Firstname", max_length=50)
    lastname: str = Field(..., title="Lastname", max_length=50)
    email: EmailStr = Field(..., title="Email", max_length=128)


class Goods(BaseModel):
    id_good: int
    name: str = Field(..., title="Name", max_length=128)
    price: float = Field(0, title="Price")
    description: str = Field(None, title="Description", max_length=128)


class GoodsIn(BaseModel):
    name: str = Field(..., title="Name", max_length=128)
    price: float = Field(0, title="Price")
    description: str = Field(None, title="Description", max_length=128)


class Orders(BaseModel):
    id_order: int
    id_good: int
    id_user: int
    data_order: datetime.date = Field(current_datetime.date(), title="Data order")
    status: bool = Field(None, title="Status order")


class OrdersIn(BaseModel):
    id_good: int
    id_user: int
    data_order: datetime.date = Field(current_datetime.date(), title="Data order")
    status: bool = Field(None, title="Status order")
