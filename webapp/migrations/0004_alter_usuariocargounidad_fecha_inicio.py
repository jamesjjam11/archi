# Generated by Django 4.2 on 2024-08-13 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_bitacora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariocargounidad',
            name='fecha_inicio',
            field=models.DateField(auto_now_add=True),
        ),
    ]
