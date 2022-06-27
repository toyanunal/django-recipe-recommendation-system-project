from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

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
    path('recipe_list/',views.recipe_form_view,name='recipe_list'),
    path('recipe_list/<str:slug>/',views.recipe_detail_view,name='recipe_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
