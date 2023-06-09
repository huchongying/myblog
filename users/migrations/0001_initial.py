# Generated by Django 4.1 on 2023-04-23 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                    "nike_name",
                    models.CharField(
                        blank=True, default="", max_length=50, verbose_name="昵称"
                    ),
                ),
                (
                    "birthday",
                    models.DateField(blank=True, null=True, verbose_name="生日"),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("male", "男"), ("female", "女")],
                        max_length=6,
                        verbose_name="性别",
                    ),
                ),
                (
                    "adress",
                    models.CharField(blank=True, max_length=100, verbose_name="地址"),
                ),
                (
                    "image",
                    models.ImageField(
                        default="image/default.png",
                        upload_to="image/%Y/%m",
                        verbose_name="用户头像",
                    ),
                ),
                (
                    "owner",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "用户数据",
                "verbose_name_plural": "用户数据",
            },
        ),
    ]
