from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('faq/', views.faq, name='faq'),
    path('input_form/', views.input_form_view, name='input_form'),
    path('pantry_create/',views.useringredient_form_view,name='pantry_create'),
    path('recipe_search/', views.IngredientListView.as_view(), name='recipe_search'),
    path('recipe_list/',views.RecipeListView.as_view(),name='recipe_list'),
    path('recipe_list/<str:slug>/',views.RecipeDetailView.as_view(),name='recipe_detail'),
]
