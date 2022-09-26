import sqlite3
from sqlite3 import Connection
from typing import Union

from bot.database.models.product import Product
from bot.database.models.user import User


def get_product(id: int) -> Union[Product, None]:
    product = None
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"SELECT * FROM products WHERE id={id}")
        record = cursor.fetchone()
        product = record
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
    if product is not None: return Product(product[1], product[2], product[3])


def get_user(tg_id: int) -> Union[User, None]:
    user = None
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE tg_id={tg_id}")
        record = cursor.fetchone()
        user = record
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
    if user is not None: return User(user[0], user[1])
    else: return None
