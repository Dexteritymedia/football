# Generated by Django 4.2 on 2024-04-23 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_season_alter_player_other_name_clubpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubpoint',
            name='outcome',
            field=models.CharField(choices=[('W', 'Win'), ('D', 'Draw'), ('L', 'Lose')], max_length=10),
        ),
        migrations.AlterField(
            model_name='clubpoint',
            name='point',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
