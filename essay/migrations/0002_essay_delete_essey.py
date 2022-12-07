# Generated by Django 4.1.4 on 2022-12-07 10:19

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("essay", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Essay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "identity",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="标识",
                    ),
                ),
                ("title", models.CharField(max_length=140, verbose_name="标题")),
                ("content", models.TextField(max_length=50000, verbose_name="内容")),
                ("tags", models.JSONField(blank=True, default=list, verbose_name="标签")),
                (
                    "publish_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="发布时间"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="最后更新时间"),
                ),
            ],
            options={
                "verbose_name": "随笔",
                "verbose_name_plural": "随笔",
            },
        ),
        migrations.DeleteModel(
            name="Essey",
        ),
    ]