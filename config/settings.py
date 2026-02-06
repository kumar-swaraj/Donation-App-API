import os

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')

if not settings_module:
    msg = (
        'DJANGO_SETTINGS_MODULE is not set. '
        'Expected one of: config.settings.dev | prod | test'
    )
    raise RuntimeError(msg)

from django.conf import settings  # noqa: E402, F401
