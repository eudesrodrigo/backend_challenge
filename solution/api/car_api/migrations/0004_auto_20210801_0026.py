# Generated by Django 3.1.2 on 2021-08-01 00:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_api', '0003_auto_20210801_0003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='car_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='car',
            name='gas_count',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1)]),
        ),
    ]
