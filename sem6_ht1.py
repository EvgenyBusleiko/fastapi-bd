import random

import databases
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import ForeignKey
from typing import List
from user_for_shop import User, UserIn
from goods_for_shop import Goods, GoodsIn
from orders_for_shop import Order, OrderIn
from faker import Faker
import datetime
from sqlalchemy.orm import relationship

DATABASE_URL = "sqlite:///shop_database.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(32)),
    sqlalchemy.Column("lastname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
)
goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("discription", sqlalchemy.String(128)),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("users.id")),
    sqlalchemy.Column("good_id", sqlalchemy.Integer, ForeignKey("goods.id")),
    sqlalchemy.Column("order_date", sqlalchemy.String(18)),
    sqlalchemy.Column("order_status", sqlalchemy.String(10)),

)
engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

fake = Faker("ru_RU")

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/fake_users/{count}")
async def create_fake_users(count: int):
    for i in range(count):
        username = fake.first_name()
        lastname = fake.last_name()

        email = fake.unique.email()
        password = fake.password()
        query = users.insert().values(username=username, lastname=lastname, email=email, password=password)
        await database.execute(query)
    return {'message': f'{count} fake users create'}


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.get("/fake_goods/{count}")
async def create_fake_goods(count: int):
    for i in range(count):
        name = f'Good_{i}'
        discription = fake.text(max_nb_chars=30)
        price = float(random.randint(1, 100))
        query = goods.insert().values(name=name, discription=discription, price=price)
        await database.execute(query)
    return {'message': f'{count} fake goods create'}


@app.post("/goods/", response_model=Goods)
async def create_goods(good: GoodsIn):
    query = goods.insert().values(**good.dict())
    last_record_id = await database.execute(query)
    return {**good.dict(), "id": last_record_id}


@app.get("/goods/", response_model=List[Goods])
async def read_goods():
    query = goods.select()
    return await database.fetch_all(query)


@app.put("/goods/{goods_id}", response_model=Goods)
async def update_goods(goods_id: int, new_goods: GoodsIn):
    query = goods.update().where(goods.c.id == goods_id).values(**new_goods.dict())
    await database.execute(query)
    return {**new_goods.dict(), "id": goods_id}


@app.delete("/goods/{goods_id}")
async def delete_goods(goods_id: int):
    query = goods.delete().where(goods.c.id == goods_id)
    await database.execute(query)
    return {'message': 'Goods deleted'}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.dict())
    print(order)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{search_id}", response_model=List[Order])
async def read_orders_by_user(search_id: int):
    query = orders.select().where(orders.c.user_id == search_id)
    return await database.fetch_all(query)


@app.get("/orders/{good_id}", response_model=List[Order])
async def read_orders_by_goods(good_id: int):
    query = orders.select().where(orders.c.good_id == good_id)
    return await database.fetch_all(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
