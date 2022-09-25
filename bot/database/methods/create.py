import random
import sqlite3
from random import random

from bot.database.models.order import Order
from bot.database.models.user import User


def create_user(tg_id: int) -> User:
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"INSERT INTO users VALUES(0, {tg_id})")
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
    return User(tg_id, 0)


def create_order(tg_id: int, address: str, comment: str, phone: str, product: int) -> Order:
    order_id = 0
    code = random.randint(10000, 99999)
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        d = cursor.execute(f"INSERT INTO orders (address, comment, phone, product, state, tg_id, code) "
                           f"VALUES('{address}', '{comment}', '{phone}', {product}, 0, {tg_id}, {code})")
        order_id = d.lastrowid
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
    if order_id != 0:
        return Order(order_id, product, tg_id, address, comment, phone, 0, code)
