# Generated by Django 4.2.3 on 2024-05-21 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_team_league'),
    ]

    operations = [
        migrations.CreateModel(
            name='BirthYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerNationality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=100, unique=True)),
                ('country_code', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': "Player's Nationalities",
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='date_of_birth',
            field=models.DateField(blank=True),
        ),
        migrations.CreateModel(
            name='PlayerRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(help_text="Player's age at this particular season")),
                ('match_played', models.PositiveIntegerField()),
                ('starts', models.PositiveIntegerField()),
                ('minutes_played', models.PositiveIntegerField()),
                ('goals', models.PositiveIntegerField()),
                ('assists', models.PositiveIntegerField()),
                ('card_yellow', models.PositiveIntegerField()),
                ('card_red', models.PositiveIntegerField()),
                ('penalty', models.PositiveIntegerField(help_text='Total number of penalties scored')),
                ('goals_assist', models.PositiveIntegerField(help_text='Total number of goals and assits')),
                ('goals_penalty', models.PositiveIntegerField(help_text='Total number of penalties and goals')),
                ('club', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.team')),
                ('player', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.player')),
                ('position', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.position')),
                ('season', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.season')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='nationality',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.playernationality'),
        ),
        migrations.AddField(
            model_name='player',
            name='year_of_birth',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.birthyear'),
        ),
    ]