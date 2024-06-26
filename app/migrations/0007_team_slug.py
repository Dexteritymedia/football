# Generated by Django 4.2 on 2024-04-26 21:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_team_options_team_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, null=True),
        ),
    ]
