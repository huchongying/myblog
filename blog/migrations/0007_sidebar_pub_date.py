# Generated by Django 4.1 on 2023-04-26 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_remove_sidebar_is_hot_sidebar_pv"),
    ]

    operations = [
        migrations.AddField(
            model_name="sidebar",
            name="pub_date",
            field=models.DateTimeField(auto_now=True, verbose_name="修改时间"),
        ),
    ]
