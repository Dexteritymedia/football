# Generated by Django 4.2.3 on 2024-05-21 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_player_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playernationality',
            name='country_code',
            field=models.CharField(max_length=20),
        ),
    ]
