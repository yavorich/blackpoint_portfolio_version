from django.db.models import (
    Model,
    CharField,
    ManyToManyField,
    BooleanField,
    ForeignKey,
    SET_NULL,
)

from .tariff import SubscriptionTariff
from .city import City


class Place(Model):
    is_active = BooleanField("Активен", default=True)
    name = CharField("Название", max_length=50, blank=True, null=True)
    city = ForeignKey(
        City,
        related_name="places",
        verbose_name="Город",
        blank=True,
        null=True,
        on_delete=SET_NULL,
    )
    address = CharField("Адрес автомата", max_length=255)
    # tariffs = ManyToManyField(
    #     SubscriptionTariff,
    #     related_name="places",
    #     verbose_name="Доступные тарифы",
    #     blank=True,
    # )
    # point = PointField("Координаты", geography=True, srid=4326)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "автомат"
        verbose_name_plural = "Автоматы"
        ordering = ["address"]
