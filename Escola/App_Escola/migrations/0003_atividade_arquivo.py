# Generated by Django 5.0.4 on 2024-04-25 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Escola', '0002_alter_atividade_id_turma'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to='atividade_arquivo/'),
        ),
    ]
