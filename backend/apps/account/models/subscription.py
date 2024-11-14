from enum import Enum
from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
    DateField,
    PositiveIntegerField,
    CharField,
)
from django.utils.timezone import localdate

from .user import User


class BaseSubscription(Model):
    description = CharField("Описание", max_length=100)
    price = PositiveIntegerField("Цена (в рублях)", default=1990)
    duration_days = PositiveIntegerField("Кол-во дней", default=30)


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"


class UserSubscription(Model):
    user = ForeignKey(User, related_name="user_subscriptions", on_delete=CASCADE)
    place = ForeignKey(
        "vending.Place", related_name="user_subscriptions", on_delete=CASCADE
    )
    expire_date = DateField("Дата истечения")

    @property
    def status(self):
        if self.expire_date >= localdate():
            return SubscriptionStatus.ACTIVE
        return SubscriptionStatus.EXPIRED


class SubscriptionPayment(Model):
    user = ForeignKey(User, related_name="payments", on_delete=CASCADE)
    place = ForeignKey("vending.Place", related_name="payments", on_delete=CASCADE)
    price = PositiveIntegerField("Стоимость")
