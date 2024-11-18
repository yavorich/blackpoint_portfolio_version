from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    PositiveIntegerField,
    CASCADE,
    DateTimeField,
)
from apps.account.models import User


class DrinkType(Model):
    name = CharField("Название напитка", max_length=100, unique=True)

    class Meta:
        verbose_name = "напиток"
        verbose_name_plural = "Напитки"

    def __str__(self):
        return self.name


class DrinkVolume(Model):
    drink_type = ForeignKey(
        DrinkType, on_delete=CASCADE, related_name="volumes", verbose_name="Напиток"
    )
    volume_ml = PositiveIntegerField("Объём (мл)")
    price = PositiveIntegerField("Цена")

    class Meta:
        verbose_name = "объём"
        verbose_name_plural = "Объёмы напитков"
        unique_together = (
            "drink_type",
            "volume_ml",
        )

    def __str__(self):
        return f"{self.drink_type} - {self.volume_ml} мл"


class DrinkHistory(Model):
    drink = ForeignKey(
        DrinkVolume, related_name="history", verbose_name="Напиток", on_delete=CASCADE
    )
    place = ForeignKey(
        "vending.Place",
        related_name="drink_history",
        verbose_name="Автомат",
        on_delete=CASCADE,
    )
    user = ForeignKey(
        User,
        related_name="drink_history",
        verbose_name="Пользователь",
        on_delete=CASCADE,
    )
    purchased_at = DateTimeField("Дата покупки", auto_now_add=True)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "История заказов"

    def __str__(self):
        return str(self.drink)

    @property
    def drink_name(self):
        return f"{self.drink.drink_type.name} {self.drink.volume_ml} мл"

    @property
    def place_address(self):
        return f"{self.place.city.name}, {self.place.address}"

    @property
    def purchase_date(self):
        return self.purchased_at.date()
