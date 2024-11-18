from django.db.models import Model, CharField


class Partner(Model):
    name = CharField("Название партнёра", max_length=127)

    class Meta:
        verbose_name = "партнёра"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name
