# Generated by Django 3.2.5 on 2022-05-30 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrs_app', '0008_auto_20220530_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True),
        ),
    ]