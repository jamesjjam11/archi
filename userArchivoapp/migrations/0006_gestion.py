# Generated by Django 4.2 on 2024-11-05 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userArchivoapp', '0005_alter_prestamo_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('año', models.CharField(max_length=4, unique=True)),
                ('abierta', models.BooleanField(default=True)),
            ],
        ),
    ]
