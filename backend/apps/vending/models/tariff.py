from django.db.models import Model, CharField, PositiveIntegerField


class SubscriptionTariff(Model):
    name = CharField("Описание", max_length=100)
    days = PositiveIntegerField("Кол-во дней")
    cups = PositiveIntegerField("Кол-во чашек в день")
    price = PositiveIntegerField("Цена (в рублях)")

    def __str__(self):
        return self.name
