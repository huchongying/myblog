# Generated by Django 4.1 on 2023-04-25 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_sidebar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sidebar",
            name="title",
            field=models.CharField(max_length=50, verbose_name="模块名称"),
        ),
    ]
