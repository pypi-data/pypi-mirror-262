# Django Log Shortcut

Install the package

```bash
pip install tms_django_config
```

Add the application in the `INSTALLE_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'tms_django_config',
    ...
]
```

Apply migrations

```python
python manage.py migrate
```

Then use the shortcut
```python
from tms_django_config.models import Config, ConfigType

my_config, _ = Config.objects.get_or_create(key="my-config-key", defaults=dict(type=ConfigType.TEXT, value="My default value"))

config_value = my_config.to_value()
```

