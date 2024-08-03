from typing import List, Union
from fastapi import APIRouter, HTTPException, Query, Path

from the_flask_and_fastapi_framework.dz.dz_6_dop_vozm_fastapi.db import (
    users,
    database,
    goods,
    orders,
    DataType,
    insert_into_table,
    fetch_by_id, update_and_fetch_by_id,
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


@router.post("/users/", response_model=User)
async def create_user(user: UserIn):
    return await insert_into_table("users", user)


@router.post("/goods/", response_model=Goods)
async def create_goods(good: GoodsIn):
    return await insert_into_table("goods", good)


@router.post("/orders/", response_model=Orders)
async def create_order(order: OrdersIn):
    return await insert_into_table("orders", order)


@router.get(
    "/data/{type}/", response_model=Union[List[User], List[Goods], List[Orders]]
)
async def read_data(
        type: DataType = Path(..., description="Type of data to retrieve:")
):
    if type == "users":
        return await database.fetch_all(users.select())
    elif type == "goods":
        return await database.fetch_all(goods.select())
    elif type == "orders":
        return await database.fetch_all(orders.select())
    else:
        raise HTTPException(status_code=400, detail="Invalid data type")


@router.get("/users/{id_user}", response_model=User)
async def read_user(user_id: int):
    return await fetch_by_id(users, user_id, User)


@router.get("/goods/{id_good}", response_model=Goods)
async def read_good(good_id: int):
    return await fetch_by_id(goods, good_id, Goods)


@router.get("/orders/{id_order}", response_model=Orders)
async def read_order(order_id: int):
    return await fetch_by_id(orders, order_id, Orders)


@router.put("/users/{id_user}", response_model=User)
async def update_user(id_user: int, new_user: UserIn):
    return await update_and_fetch_by_id(users, id_user, new_user.dict(), User)


@router.put("/goods/{id_good}", response_model=Goods)
async def update_good(id_good: int, new_good: GoodsIn):
    return await update_and_fetch_by_id(goods, id_good, new_good.dict(), Goods)


@router.put("/orders/{id_order}", response_model=Orders)
async def update_order(id_order: int, new_order: OrdersIn):
    return await update_and_fetch_by_id(orders, id_order, new_order.dict(), Orders)


@router.delete("/users/{id_user}")
async def delete_user(user_id: int):
    result = await database.fetch_one(users.select().where(users.c.id == user_id))
    if result is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    await database.execute(users.delete().where(users.c.id == user_id))
    return {"message": f"User {user_id} deleted"}


@router.delete("/goods/{id_good}")
async def delete_good(good_id: int):
    result = await database.fetch_one(goods.select().where(goods.c.id == good_id))
    if result is None:
        raise HTTPException(status_code=404, detail=f"Good with id {good_id} not found")
    await database.execute(goods.delete().where(goods.c.id == good_id))
    return {"message": f"Good {good_id} deleted"}


@router.delete("/orders/{id_order}")
async def delete_order(order_id: int):
    result = await database.fetch_one(orders.select().where(orders.c.id == order_id))
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found"
        )
    await database.execute(orders.delete().where(orders.c.id == order_id))
    return {"message": f"Order {order_id} deleted"}
