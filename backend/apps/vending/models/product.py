# from django.db.models import Model, CharField, ForeignKey, PositiveIntegerField, FloatField, CASCADE


# class DrinkType(Model):
#     name = CharField(max_length=100, unique=True)  # Название типа напитка (например, "Кофе", "Чай")

#     def __str__(self):
#         return self.name


# class DrinkVolume(Model):
#     drink_type = ForeignKey(DrinkType, on_delete=CASCADE, related_name='volumes')
#     volume_ml = PositiveIntegerField()  # Объём в миллилитрах (например, 250, 500)
#     price = FloatField(max_digits=5, decimal_places=2)  # Цена за данный объем напитка

#     class Meta:
#         unique_together = ('drink_type', 'volume_ml')  # Запретим дублирование одного и того же объема для типа

#     def __str__(self):
#         return f"{self.volume_ml} ml"