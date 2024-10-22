from enum import Enum


class OrderTypeEnum(Enum):
    Normal = "normal"
    Express = "express"


class OrderStatusEnum(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    FINISHED = "finished"
    values = [PENDING, CONFIRMED, CANCELED, FINISHED]
