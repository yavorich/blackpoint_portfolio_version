from django.db.models import Model, CharField, PositiveIntegerField, BooleanField


class SubscriptionTariff(Model):
    is_active = BooleanField("Активен", default=True)
    name = CharField("Название тарифа", max_length=100)
    days = PositiveIntegerField("Кол-во дней")
    cups = PositiveIntegerField("Кол-во чашек в день")
    price = PositiveIntegerField("Цена (в рублях)")

    class Meta:
        verbose_name = "тариф"
        verbose_name_plural = "Тарифы абонементов"

    def __str__(self):
        return self.name
