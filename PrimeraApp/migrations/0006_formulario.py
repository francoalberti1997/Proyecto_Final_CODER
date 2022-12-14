# Generated by Django 4.1.1 on 2022-11-26 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PrimeraApp', '0005_remove_profile_tiene_experiencia_profile_usuario_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('mail', models.EmailField(max_length=50)),
                ('celular', models.CharField(max_length=50)),
                ('curso', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PrimeraApp.cursos')),
            ],
        ),
    ]
