# Generated by Django 4.2 on 2024-05-09 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_season_name_alter_season_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
