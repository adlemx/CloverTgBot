import sqlite3

from bot.database.models.product import Product


def get_product(id: int) -> Product:
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
