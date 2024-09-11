# Generated by Django 4.2.3 on 2024-09-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_customerpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpayment',
            name='expiry_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='customerpayment',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]