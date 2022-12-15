"""essay_viewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def _prefixed(pattern):
    if not settings.URL_PREFIX or settings.URL_PREFIX.strip() == "/":
        return pattern
    url_prefix = settings.URL_PREFIX.lstrip("/")
    if not url_prefix.endswith("/"):
        url_prefix += "/"
    return url_prefix + pattern


urlpatterns = [
    path("", lambda r: redirect("root")),
    path(_prefixed(""), lambda r: redirect("essay:index"), name="root"),
    path(_prefixed("accounts/"), include("allauth.urls")),
    path(_prefixed("admin/"), admin.site.urls),
    path(_prefixed("essay/"), include("essay.urls")),
]
