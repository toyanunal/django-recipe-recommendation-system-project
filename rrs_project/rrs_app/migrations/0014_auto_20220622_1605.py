# Generated by Django 3.2.5 on 2022-06-22 13:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rrs_app', '0013_auto_20220622_1340'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipeingredient',
            name='unique_recipeingredient',
        ),
        migrations.RemoveConstraint(
            model_name='useringredient',
            name='unique_useringredient',
        ),
        migrations.AlterUniqueTogether(
            name='recipeingredient',
            unique_together={('recipe', 'ingredient')},
        ),
        migrations.AlterUniqueTogether(
            name='useringredient',
            unique_together={('user', 'ingredient')},
        ),
    ]