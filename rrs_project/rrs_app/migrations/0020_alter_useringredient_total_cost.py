# Generated by Django 3.2.5 on 2022-06-26 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrs_app', '0019_alter_useringredient_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useringredient',
            name='total_cost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]