# Generated by Django 3.2.5 on 2022-06-26 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrs_app', '0017_useringredient_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useringredient',
            name='total_cost',
            field=models.FloatField(null=True),
        ),
    ]