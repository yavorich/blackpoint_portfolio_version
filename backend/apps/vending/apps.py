from django.apps import AppConfig


class VendingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.vending"
    verbose_name = "Точка Чёрного"

    def ready(self):
        import apps.vending.signals
