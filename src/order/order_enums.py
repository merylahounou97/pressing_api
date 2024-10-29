from enum import Enum


class OrderTypeEnum(Enum):
    NORMAL = "NORMAL"
    EXPRESS = "EXPRESS"


class OrderStatusEnum(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    FINISHED = "FINISHED"
    # values = [PENDING, CONFIRMED, CANCELED, FINISHED]
