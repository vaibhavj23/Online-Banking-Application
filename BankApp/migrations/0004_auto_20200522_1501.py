# Generated by Django 3.0.6 on 2020-05-22 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankApp', '0003_auto_20200521_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='fixed_acc',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='account',
            name='saving_acc',
            field=models.CharField(max_length=50),
        ),
    ]
