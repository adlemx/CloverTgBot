class Product(object):
    name = ""
    description = ""
    price = 0

    def __init__(self, name: str, description: str, price: int):
        """ :param name: Названия товара
            :param description: Описания товара
            :param price: Цена в копейках
        """
        self.name = name
        self.description = description
        self.price = price
