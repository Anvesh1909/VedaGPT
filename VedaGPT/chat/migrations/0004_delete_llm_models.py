# Generated by Django 5.0.5 on 2024-05-24 09:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0003_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="LLM_models",
        ),
    ]