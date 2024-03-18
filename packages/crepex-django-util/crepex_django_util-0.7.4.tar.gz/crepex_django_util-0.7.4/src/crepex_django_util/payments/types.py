from enum import Enum


class PaymentType(Enum):
    """
    결제수단
    """

    card = 'card'
    transfer = 'transfer'
