import uuid
from django.db import models
from django.utils import timezone


class Essay(models.Model):
    identity = models.UUIDField("标识", default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField("标题", max_length=140)
    content = models.TextField("内容", max_length=50_000)
    tags = models.JSONField("标签", blank=True, default=list)
    publish_date = models.DateTimeField("发布时间", default=timezone.now)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("最后更新时间", auto_now=True)

    class Meta:
        verbose_name = "随笔"
        verbose_name_plural = verbose_name
