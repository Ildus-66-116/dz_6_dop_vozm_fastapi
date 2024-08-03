import sqlalchemy
from the_flask_and_fastapi_framework.seminars.sem_6_dop_vozm_fastapi.db import database


async def create(name_table: sqlalchemy.Table, value_table, name_column: str):
    query = name_table.insert().values(**value_table.dict())
    last_record_id = await database.execute(query)
    return {**value_table.dict(), f'"{name_column}"': last_record_id}
