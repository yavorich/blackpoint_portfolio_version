from enum import Enum
from django.db.models import (
    CASCADE,
    DateField,
    ForeignKey,
    Model,
    PositiveIntegerField,
)
from django.utils.timezone import localdate

from apps.vending.models import SubscriptionTariff, Place

from .user import User


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"


class UserSubscription(Model):
    user = ForeignKey(User, related_name="user_subscriptions", on_delete=CASCADE)
    place = ForeignKey(
        Place, related_name="user_subscriptions", on_delete=CASCADE
    )
    tariff = ForeignKey(
        SubscriptionTariff,
        related_name="user_subscriptions",
        blank=True,
        null=True,
        on_delete=CASCADE,
    )
    start_date = DateField("Дата начала")
    expire_date = DateField("Дата истечения")
    today_cups = PositiveIntegerField("Осталось чашек на сегодня")

    @property
    def status(self):
        if self.expire_date >= localdate():
            return SubscriptionStatus.ACTIVE
        return SubscriptionStatus.EXPIRED


class SubscriptionPayment(Model):
    user = ForeignKey(User, related_name="payments", on_delete=CASCADE)
    place = ForeignKey("vending.Place", related_name="payments", on_delete=CASCADE)
    tariff = ForeignKey(
        SubscriptionTariff,
        related_name="payments",
        blank=True,
        null=True,
        on_delete=CASCADE,
    )
