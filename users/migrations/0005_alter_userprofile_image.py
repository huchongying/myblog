# Generated by Django 4.1 on 2023-04-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_userprofile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="image",
            field=models.ImageField(
                default="images/2023/04/img.jpg",
                upload_to="images/%Y/%m/",
                verbose_name="用户头像",
            ),
        ),
    ]