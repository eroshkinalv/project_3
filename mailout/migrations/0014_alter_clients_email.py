# Generated by Django 5.1.3 on 2025-01-02 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailout", "0013_alter_clients_options_alter_mailout_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clients",
            name="email",
            field=models.CharField(max_length=150, verbose_name="Email"),
        ),
    ]
