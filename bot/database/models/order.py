import types


class Order(object):
    order_id: int
    product: int
    comment: str
    address: str = ""
    phone: str = ""
    state: int = 0 # 0 - pre order; 1 - payment required; 2 - assembling; 3 - delivery; 4 - done;
    tg_id: int = 0

    def __init__(self, order_id: int, product: int, tg_id: int, address: str,  comment: str, phone: str, state: int):
        self.order_id = order_id
        self.product = product
        self.comment = comment
        self.tg_id = tg_id
        self.address = address
        self.phone = phone
        self.state = state

    