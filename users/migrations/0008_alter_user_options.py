# Generated by Django 5.1.3 on 2025-01-06 02:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_remove_user_groups_user_groups"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "permissions": [("manager", "Can view and block users")],
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]
