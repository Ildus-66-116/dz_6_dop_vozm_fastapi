from typing import Type

import databases
import sqlalchemy
from enum import Enum

from fastapi import HTTPException
from sqlalchemy import select

from settings import settings

DATABASE_URL = settings.DATABASE_URL

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("firstname", sqlalchemy.String(50)),
    sqlalchemy.Column("lastname", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(128)),
    sqlalchemy.Column("price", sqlalchemy.FLOAT),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
)
orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "id_good", sqlalchemy.Integer, sqlalchemy.ForeignKey(goods.c.id)
    ),
    sqlalchemy.Column(
        "id_user", sqlalchemy.Integer, sqlalchemy.ForeignKey(users.c.id)
    ),
    sqlalchemy.Column("data_order", sqlalchemy.DATE),
    sqlalchemy.Column("status", sqlalchemy.BOOLEAN),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)


class DataType(str, Enum):
    users = "users"
    goods = "goods"
    orders = "orders"


async def insert_into_table(table_name_str: str, item: dict):
    values_dict = item.dict()
    table_object = metadata.tables[table_name_str]
    query = table_object.insert().values(**values_dict)
    last_record_id = await database.execute(query)
    return {**values_dict, "id": last_record_id}


async def fetch_by_id(table_name: str, id_value: int, model: Type):
    stmt = select(table_name).where(table_name.c.id == id_value)
    result = await database.fetch_one(stmt)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} with id {id_value} not found")
    return result


