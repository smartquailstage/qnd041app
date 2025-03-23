# Generated by Django 4.2.20 on 2025-03-23 16:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0002_dashboard_remove_profile_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edificio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.CharField(blank=True, max_length=255, null=True, verbose_name='Especialidad')),
                ('presupuesto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Presupuesto del Edificio')),
                ('k', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(10)], verbose_name='Factor K')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Nombre de Usuario')),
            ],
            options={
                'verbose_name_plural': 'Perfil de Edificios',
                'ordering': ['user'],
            },
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_terapeuta',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='usuarios.edificio', verbose_name='Terapeuta Asignado'),
        ),
        migrations.DeleteModel(
            name='Perfil_Terapeuta',
        ),
    ]
