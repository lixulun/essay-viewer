from django.contrib import admin
from essay import models


@admin.register(models.Essay)
class EsseyAdmin(admin.ModelAdmin):
    list_display = (
        "identity",
        "title",
        "content",
        "tags",
        "publish_date",
    )
    date_hierarchy = "publish_date"
