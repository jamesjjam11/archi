# Generated by Django 4.2 on 2024-09-23 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userArchivoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(choices=[('fisico', 'Físico'), ('digital', 'Digital')], default='fisico', max_length=10)),
                ('fecha_prestamo', models.DateField(auto_now_add=True)),
                ('fecha_devolucion', models.DateField(blank=True, null=True)),
                ('estado_prestamo', models.BooleanField(default=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userArchivoapp.documento')),
                ('usuario_prestamo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]