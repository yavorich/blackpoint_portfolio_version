from enum import Enum
from django.db.models import (
    CASCADE,
    SET_NULL,
    DateField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    BooleanField,
)
from django.utils.timezone import localdate

from apps.vending.models import SubscriptionTariff, Place

from .user import User


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"


class UserSubscription(Model):
    user = ForeignKey(
        User,
        related_name="user_subscriptions",
        verbose_name="Пользователь",
        on_delete=CASCADE,
    )
    place = ForeignKey(
        Place,
        related_name="user_subscriptions",
        verbose_name="Автомат",
        on_delete=CASCADE,
    )
    tariff = ForeignKey(
        SubscriptionTariff,
        related_name="user_subscriptions",
        verbose_name="Тариф",
        blank=True,
        null=True,
        on_delete=CASCADE,
    )
    start_date = DateField("Дата начала")
    expire_date = DateField("Дата истечения")
    today_cups = PositiveIntegerField("Осталось чашек на сегодня")

    class Meta:
        verbose_name = "абонемент"
        verbose_name_plural = "Абонементы пользователя"
        ordering = ["expire_date"]  # не менять

    def __str__(self):
        return f"{self.tariff.name} - {self.place.address}"

    @property
    def status(self):
        if self.expire_date >= localdate():
            return SubscriptionStatus.ACTIVE
        return SubscriptionStatus.EXPIRED


class SubscriptionPayment(Model):
    subscription = ForeignKey(
        UserSubscription,
        related_name="payments",
        verbose_name="Абонемент",
        on_delete=SET_NULL,
        null=True,
    )
    user = ForeignKey(
        User,
        related_name="payments",
        verbose_name="Пользователь",
        null=True,
        on_delete=SET_NULL,
    )
    place = ForeignKey(
        "vending.Place",
        related_name="payments",
        verbose_name="Место",
        null=True,
        on_delete=SET_NULL,
    )
    tariff = ForeignKey(
        SubscriptionTariff,
        related_name="payments",
        verbose_name="Тариф",
        null=True,
        on_delete=SET_NULL,
    )
    price = PositiveIntegerField(verbose_name="Стоимость")
    payment_date = DateField("Дата платежа", blank=True, null=True)

    class Meta:
        verbose_name = "платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платёж №{self.id}"
