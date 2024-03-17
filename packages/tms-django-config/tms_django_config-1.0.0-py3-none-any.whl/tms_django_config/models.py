from datetime import date, datetime
from django.utils.translation import gettext, gettext_lazy as _
from django.db import models


class ConfigType(models.TextChoices):
    TEXT = "T", _("Text")
    BOOL = "B", _("Boolean")
    INT = "I", _("Integer")
    FLOAT = "F", _("Float")
    DATE = "D", _("Date")
    DATETIME = "M", _("Datetime")
    ARRAY = "A", _("Array")


class Config(models.Model):
    key = models.SlugField(max_length=128, primary_key=True)
    value = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=1, choices=ConfigType.choices, default=ConfigType.TEXT
    )

    def __str__(self):
        return f"{self.to_value()}"

    def to_value(self):
        if self.type == ConfigType.TEXT:
            return self.value
        if self.type == ConfigType.INT:
            return int(self.value)
        if self.type == ConfigType.BOOL:
            return self.value.lower() == "true"
        if self.type == ConfigType.FLOAT:
            return float(self.value)
        if self.type == ConfigType.DATE:
            return datetime.fromisoformat(self.value)
        if self.type == ConfigType.DATETIME:
            return datetime.fromisoformat(self.value)
        if self.type == ConfigType.ARRAY:
            return self.value.split(",")
