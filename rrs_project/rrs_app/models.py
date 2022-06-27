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
    photo = models.ImageField(blank=True, upload_to='ingredient_photos/')

    class Meta:
        ordering = ('title',)

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
    photo = models.ImageField(blank=True, upload_to='recipe_photos/')

    class Meta:
        ordering = ('title',)

    def get_absolute_url(self):
        '''
        This tells Django how to calculate the URL for an object.
        Django uses this in its admin interface, and any time it needs to figure out a URL for an object.
        Any object that has a URL that uniquely identifies it should define this method.
        '''
        return reverse("recipe_detail", kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])

    class Meta:
        unique_together = (('recipe', 'ingredient'))
        ordering = ('recipe','ingredient')

    def __str__(self):
        return str(self.recipe) + "#" + str(self.ingredient) + "#" + str(self.amount)

class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    total_cost = models.FloatField(default=0, blank=True)

    class Meta:
        unique_together = (('user', 'ingredient'))
        ordering = ('user','ingredient')

    def __str__(self):
        return str(self.user) + "#" + str(self.ingredient) + "#" + str(self.amount)

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addcost = models.FloatField(default=0)
    portion = models.FloatField(default=1)

    def __str__(self):
        return str(self.user) + "#" + str(self.addcost) + "#" + str(self.portion)
