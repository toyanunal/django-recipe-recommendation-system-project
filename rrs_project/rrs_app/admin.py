from django.contrib import admin
from .models import Recipe,Ingredient,RecipeIngredient,UserIngredient,UserInfo

# Register your models here.

# toyanunal : toyanunalpassword

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(UserIngredient)
admin.site.register(UserInfo)
