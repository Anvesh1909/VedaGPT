# Generated by Django 5.0.3 on 2024-03-16 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_remove_transaction_doc_delete_documents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file_path', models.CharField(max_length=255)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.chat')),
            ],
        ),
    ]
