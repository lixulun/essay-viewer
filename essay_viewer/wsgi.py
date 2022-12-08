"""
WSGI config for essay_viewer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

setting_suffix = ""
env = os.getenv("ENV")
if env:
    setting_suffix = "_" + env
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "essay_viewer.settings" + setting_suffix
)

application = get_wsgi_application()
