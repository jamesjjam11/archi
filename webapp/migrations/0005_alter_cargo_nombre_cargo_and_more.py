# Generated by Django 4.2 on 2024-09-20 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_usuariocargounidad_fecha_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='nombre_cargo',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='secretaria',
            name='nombre_secretaria',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='unidad',
            name='nombre_unidad',
            field=models.CharField(max_length=200),
        ),
    ]