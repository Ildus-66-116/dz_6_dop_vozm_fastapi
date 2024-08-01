from typing import List
from fastapi import APIRouter, HTTPException
from the_flask_and_fastapi_framework.dz.dz_6_dop_vozm_fastapi.db import (
    users,
    database,
    goods,
    orders,
)
from the_flask_and_fastapi_framework.dz.dz_6_dop_vozm_fastapi.models import (
    User,
    UserIn,
    Goods,
    GoodsIn,
    Orders,
    OrdersIn,
)

router = APIRouter()


# @router.get("/fake_users/{count}")
# async def create_users(count: int):
#     for i in range(1, count + 1):
#         query = users.insert().values(
#             firstname=f"firstname{i}",
#             lastname=f"lastname{i + 10}",
#             email=f"mail{i}@mail.ru",
#             password=f"p{i}a{i + 1}s{i}s{i + 2}",
#         )
#         await database.execute(query)
#     return {"message": f"{count} fake users create"}


@router.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id_user": last_record_id}


@router.post("/goods/", response_model=Goods)
async def create_goods(good: GoodsIn):
    query = goods.insert().values(**good.dict())
    last_record_id = await database.execute(query)
    return {**good.dict(), "id_good": last_record_id}


@router.post("/orders/", response_model=Orders)
async def create_order(order: OrdersIn):
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {**order.dict(), "id_order": last_record_id}


@router.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@router.get("/goods/", response_model=List[Goods])
async def read_goods():
    query = goods.select()
    return await database.fetch_all(query)


@router.get("/orders/", response_model=List[Orders])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)
