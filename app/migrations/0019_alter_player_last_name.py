# Generated by Django 4.2.3 on 2024-05-21 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_playernationality_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]