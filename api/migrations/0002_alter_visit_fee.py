# Generated by Django 3.2.10 on 2022-01-25 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='fee',
            field=models.FloatField(default=50.0),
        ),
    ]
