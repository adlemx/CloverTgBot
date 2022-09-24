from os import environ
from typing import Final


class TgKeys:
    TOKEN: Final = environ.get('TOKEN', 'define me!')
    PAYTOKEN: Final = environ.get('PAYTOKEN', 'define me!')
