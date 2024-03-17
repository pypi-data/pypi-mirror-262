from django.apps import AppConfig


class ConfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tms_django_config"
    label = "Config"
    verbose_name = "Configurations"
