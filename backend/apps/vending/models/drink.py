from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    PositiveIntegerField,
    CASCADE,
    DateTimeField,
)
from apps.account.models import User
from core.builted.blank_and_null import blank_and_null


class DrinkType(Model):
    place = ForeignKey(
        "vending.Place",
        related_name="drinks",
        verbose_name="Автомат",
        on_delete=CASCADE,
        **blank_and_null,
    )
    name = CharField("Название напитка", max_length=100, unique=True)

    class Meta:
        verbose_name = "напиток"
        verbose_name_plural = "Меню напитков"

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

    @property
    def name(self):
        return f"{self.drink_type} - {self.volume_ml} мл"


class DrinkHistory(Model):
    place = ForeignKey(
        "vending.Place",
        related_name="drink_history",
        verbose_name="Автомат",
        on_delete=CASCADE,
        **blank_and_null,
    )
    partner = ForeignKey(
        "vending.Partner",
        related_name="drink_history",
        verbose_name="Партнёр",
        on_delete=CASCADE,
        **blank_and_null,
    )
    user = ForeignKey(
        User,
        related_name="drink_history",
        verbose_name="Пользователь",
        on_delete=CASCADE,
        **blank_and_null,
    )
    purchased_at = DateTimeField("Дата покупки", auto_now_add=True)
    price = PositiveIntegerField("Стоимость", **blank_and_null)
    drink_name = CharField("Напиток", max_length=128, **blank_and_null)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "История заказов"

    @property
    def place_address(self):
        return f"{self.place.city.name}, {self.place.address}"

    @property
    def purchase_date(self):
        return self.purchased_at.date()
