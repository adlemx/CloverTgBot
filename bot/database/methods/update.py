import sqlite3
from random import random

from bot.database.models.main import OrderStates


def new_order(tg_id: int):
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"UPDATE users SET orders_count = orders_count + 1 WHERE tg_id = {tg_id}")
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def change_order_state(order_id: int, state: OrderStates):
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"UPDATE orders SET state = {state.value} WHERE order_id = {order_id}")
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def set_address(order_id: int, location: str):
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"UPDATE orders SET address = '{location}' WHERE order_id = {order_id}")
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def set_phone(order_id: int, phone: str):
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"UPDATE orders SET phone = {phone} WHERE order_id = {order_id}")
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()