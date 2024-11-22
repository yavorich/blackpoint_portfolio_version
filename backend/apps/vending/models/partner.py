from django.db.models import Model, CharField, PositiveIntegerField

from core.builted.blank_and_null import blank_and_null


class Partner(Model):
    partner_id = PositiveIntegerField("ID партнёра", **blank_and_null)
    name = CharField("Название партнёра", max_length=127)

    class Meta:
        verbose_name = "партнёра"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name
