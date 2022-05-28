from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from autoslug import AutoSlugField

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title")
    diet_type = models.CharField(max_length=20)
    effort = models.CharField(max_length=20)
    meal_type = models.CharField(max_length=20)
    description = models.TextField()
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    photo = models.ImageField(blank=True,upload_to='rrs_app/')

    def get_absolute_url(self):
        return reverse("recipe_detail",kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    unit_type = models.CharField(max_length=20)
    unit_cost = models.FloatField(default=0)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    photo = models.ImageField(blank=True,upload_to='rrs_app/')

    def __str__(self):
        return self.title

class UserProfileInfo(models.Model): #bunu 5. dersten aldım
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.CASCADE) #primary_key=True eklenebilir
    # Add any additional attributes you want
    last_login = models.DateTimeField(default=timezone.now)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    photo = models.ImageField(upload_to='basic_app/profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User
        return self.user.username

class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return "recipe_id: " + self.recipe_id + " " + "ingredient_id: " + self.ingredient_id

class UserIngredient(models.Model):
    user_id = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return "user_id: " + self.user_id + " " + "ingredient_id: " + self.ingredient_id
