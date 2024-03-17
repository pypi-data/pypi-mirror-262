from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from tms_django_config import models


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "type")
    search_fields = ["key", "value"]
    ordering = ["key"]
