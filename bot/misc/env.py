from os import environ


class TgKeys:
    TOKEN = environ.get('TOKEN', 'define me!')
    PAYTOKEN = environ.get('PAYTOKEN', 'define me!')
