from django.db.models import Model, CharField


class City(Model):
    name = CharField("Город", max_length=127)

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "Города"
        ordering = ["name"]

    def __str__(self):
        return self.name
