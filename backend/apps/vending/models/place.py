from django.db.models import (
    Model,
    CharField,
)

# from django.contrib.gis.db.models import PointField


class Place(Model):
    address = CharField("Адрес", max_length=255)
    # point = PointField("Координаты", geography=True, srid=4326)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "место"
        verbose_name_plural = "Места"
