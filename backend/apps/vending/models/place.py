from django.core.files import File
from django.db.models import (
    Model,
    CharField,
    ManyToManyField,
    BooleanField,
    ForeignKey,
    SET_NULL,
    ImageField,
    FloatField,
    PositiveIntegerField,
)
from io import BytesIO
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L

from core.builted.blank_and_null import blank_and_null
from core.utils.get_upload_path import get_upload_path

from .city import City
from .partner import Partner
from .drink import DrinkVolume


class Place(Model):
    is_active = BooleanField("Активен", default=True)
    terminal_id = PositiveIntegerField("ID терминала", **blank_and_null)
    vendista_account = ForeignKey(
        "vending.VendistaAccount",
        related_name="terminals",
        verbose_name="Аккаунт Vendista",
        on_delete=SET_NULL,
        **blank_and_null,
    )
    name = CharField("Название", max_length=50, **blank_and_null)
    city = ForeignKey(
        City,
        related_name="places",
        verbose_name="Город",
        on_delete=SET_NULL,
        **blank_and_null,
    )
    address = CharField("Адрес автомата", max_length=255, **blank_and_null)
    latitude = FloatField("Широта", **blank_and_null)
    longitude = FloatField("Долгота", **blank_and_null)
    partner = ForeignKey(
        Partner,
        related_name="places",
        verbose_name="Партнёр",
        on_delete=SET_NULL,
        **blank_and_null,
    )
    drinks = ManyToManyField(
        DrinkVolume, related_name="places", verbose_name="Меню", blank=True
    )
    qr_code = ImageField(
        upload_to=get_upload_path(catalog="places", name_field="pk", field="qr_code"),
        **blank_and_null,
    )

    class Meta:
        verbose_name = "автомат"
        verbose_name_plural = "Автоматы"
        ordering = ["address"]

    def __str__(self):
        return self.address or "Неизвестно"

    def generate_qr_code(self):
        # Содержимое QR-кода — только ID места
        qr_data = str(self.id)
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Сохраняем QR-код в изображение
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_code.save(f"place_{self.id}.png", File(buffer), save=False)
