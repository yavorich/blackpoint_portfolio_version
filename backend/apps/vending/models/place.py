from django.db.models import (
    Model,
    CharField,
    ManyToManyField,
)

from .tariff import SubscriptionTariff


class Place(Model):
    address = CharField("Адрес", max_length=255)
    tariffs = ManyToManyField(
        SubscriptionTariff,
        related_name="places",
        blank=True,
        default=SubscriptionTariff.objects.all,
    )
    # point = PointField("Координаты", geography=True, srid=4326)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "место"
        verbose_name_plural = "Места"
