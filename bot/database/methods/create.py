import sqlite3


def create_user(tg_id: int):
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

def create_order(tg_id: int, address: str, comment: str, phone: str, product: int):
    try:
        sqlite_connection = sqlite3.connect('bot/database/db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"INSERT INTO orders (address, comment, phone, product, state, tg_id) "
                       f"VALUES('{address}', '{comment}', '{phone}', {product}, 0, {tg_id})")
        cursor.execute()
        print(cursor.fetchone())
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
