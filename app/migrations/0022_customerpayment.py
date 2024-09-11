# Generated by Django 4.2.3 on 2024-09-11 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0021_savedurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=50, null=True)),
                ('status', models.BooleanField(default=False)),
                ('credit', models.PositiveIntegerField(blank=True, null=True)),
                ('plan', models.CharField(choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=50, null=True)),
                ('subscription', models.CharField(choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')], max_length=50, null=True)),
                ('expiry_date', models.DateTimeField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
