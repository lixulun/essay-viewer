from django.urls import path
from essay import views


app_name = "essay"
urlpatterns = [
    path("", views.index, name="index"),
    path("<uuid:identity>/", views.detail, name="detail"),
]
