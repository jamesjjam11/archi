# Generated by Django 4.2 on 2024-12-05 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userArchivoapp', '0007_documento_fecha_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='numero',
            field=models.CharField(max_length=4),
        ),
    ]
