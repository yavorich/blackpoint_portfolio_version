from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import (
    BooleanField,
    DateTimeField,
    CharField,
    ImageField,
    PositiveBigIntegerField,
    UUIDField,
    ManyToManyField,
    EmailField,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.builted.blank_and_null import blank_and_null
from core.telegram.managers.user import GetByTelegramMixin
from core.utils.get_upload_path import get_upload_path


class UserManager(GetByTelegramMixin, BaseUserManager):

    def create_user(self, validated_data):
        password = validated_data.pop("password")
        username = validated_data.get("username")

        if username != "":
            if self.model.objects.filter(username=username).exists():
                raise ValueError("A user with that username already exists.")

        user = self.model(**validated_data)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        return self.create_user(
            {
                "username": username,
                "password": password,
                "is_staff": True,
            }
        )

    async def get_by_telegram(self, telegram_id):
        return await self.aget(telegram_id=telegram_id)


class User(AbstractBaseUser):
    uuid = UUIDField(default=uuid4, editable=False, unique=True)

    username_validator = UnicodeUsernameValidator()
    username = CharField(
        _("username"),
        max_length=150,
        blank=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )

    is_staff = BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    telegram_id = PositiveBigIntegerField(
        **blank_and_null, verbose_name="Telegram ID", unique=True
    )
    date_joined = DateTimeField(_("date joined"), default=timezone.now)

    first_name = CharField("Имя", max_length=255, blank=True)
    last_name = CharField("Фамилия", max_length=255, blank=True)
    avatar = ImageField(
        "Аватар",
        upload_to=get_upload_path(catalog="user", name_field="uuid", field="avatar"),
        **blank_and_null,
    )
    email = EmailField("Email", **blank_and_null)
    phone = PhoneNumberField("Номер телефона", **blank_and_null)
    subscriptions = ManyToManyField(to="vending.Place", through="UserSubscription")

    objects = UserManager()

    USERNAME_FIELD = "uuid"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self) -> str:
        return self.username or str(self.telegram_id)

    @property
    def has_active_subscriptions(self):
        return (
            self.user_subscriptions.filter(
                expire_date__gte=timezone.localdate()
            ).count()
            > 0
        )

    @property
    def subscribed_until(self):
        if self.has_active_subscriptions:
            return self.user_subscriptions.latest("expire_date").expire_date
        return None
