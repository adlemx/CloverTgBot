class User(object):
    tg_id: int
    orders: int

    def __init__(self, tg_id: int, orders: int):
        self.tg_id = tg_id
        self.orders = orders

