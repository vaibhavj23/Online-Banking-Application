# Generated by Django 3.0.6 on 2020-05-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankApp', '0004_auto_20200522_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='f_balance',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='fixed_acc',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='s_balance',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='saving_acc',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
