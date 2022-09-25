import enum


class OrderStates(enum.Enum):
    PRE_ORDER = 0
    PAYMENT_REQUIRED = 1
    ASSEMBLING = 2
    DELIVERY = 3
    DONE = 4
