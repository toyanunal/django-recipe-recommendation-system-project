from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
#1)from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    unit_type = models.CharField(max_length=16)
    unit_cost = models.FloatField(default=0)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    photo = models.ImageField(blank=True, upload_to='rrs_app/')

    def __str__(self):
        return self.title

class Recipe(models.Model):
    title = models.CharField(max_length=128)
    #1)slug = AutoSlugField(populate_from="title", unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    meal_type = models.CharField(max_length=16)
    diet_type = models.CharField(max_length=16)
    effort = models.CharField(max_length=16)
    description = models.TextField()
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    photo = models.ImageField(blank=True, upload_to='rrs_app/')

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])

    def __str__(self):
        return "recipe: " + str(self.recipe) + " - " + "ingredient: " + str(self.ingredient)

class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    #portion = models.FloatField(default=1)
    #additional_cost = models.FloatField(default=0)

    def __str__(self):
        return "user: " + str(self.user) + " - " + "ingredient: " + str(self.ingredient)
