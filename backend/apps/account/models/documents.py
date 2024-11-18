from django.db.models import Model, TextChoices, CharField, FileField

from core.builted.blank_and_null import blank_and_null
from core.utils.get_upload_path import get_upload_path


class Document(Model):
    class DocumentType(TextChoices):
        USER_AGREEMENT = "user_agreement", "Пользовательское соглашение"
        PUBLIC_OFFER = "public_offer", "Публичная оферта"
        PRIVACY_POLICY = "privacy_policy", "Политика обработки персональных данных"

    type = CharField("Тип документа", choices=DocumentType.choices, unique=True)
    file = FileField(
        "Файл",
        upload_to=get_upload_path(catalog="documents", name_field="type", field="file"),
        **blank_and_null,
    )

    class Meta:
        verbose_name = "документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.get_type_display()
