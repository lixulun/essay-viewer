"""
ASGI config for essay_viewer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

setting_suffix = ""
env = os.getenv("ENV")
if env:
    setting_suffix = "_" + env
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "essay_viewer.settings" + setting_suffix
)

application = get_asgi_application()
