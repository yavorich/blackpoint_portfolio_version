from django.db.models import (
    Model,
    ForeignKey,
    TextField,
    DateTimeField,
    CASCADE,
    BooleanField,
)
from apps.account.models import User


class SupportRequest(Model):
    user = ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="support_requests",
        on_delete=CASCADE,
    )
    message = TextField("Сообщение", max_length=500)
    created_at = DateTimeField("Дата и время", auto_now_add=True)
    viewed = BooleanField("Просмотрено", default=False)

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "Обращения в поддержку"
        ordering = ["-created_at"]

    def __str__(self):
        return f"№{self.id} от {self.user.username}"

    @classmethod
    def notify_count(cls):
        return cls.objects.filter(viewed=False).count()
