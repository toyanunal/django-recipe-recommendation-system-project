from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Recipe, Ingredient, RecipeIngredient, UserIngredient
from .forms import SignUpForm, EditProfileForm
from . import models
from . import forms

# Create your views here.
def home(request):
	return render(request, 'rrs_app/home.html', {})

def login_user(request):
	if request.method == 'POST': #if someone fills out form , Post it
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('You are logged in'))
			return redirect('home') #routes to 'home' on successful login
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'rrs_app/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('You are now logged out'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('You are now registered'))
			return redirect('home')
	else:
		form = SignUpForm()

	context = {'form': form}
	return render(request, 'rrs_app/register.html', context)

def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		#passes in user information
		form = EditProfileForm(instance= request.user)

	context = {'form': form}
	return render(request, 'rrs_app/edit_profile.html', context)

def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		#passes in user information
		form = PasswordChangeForm(user=request.user)

	context = {'form': form}
	return render(request, 'rrs_app/change_password.html', context)

def faq(request):
	return render(request, 'rrs_app/faq.html', {})

#def recipe_search(request):
#    #all_ingredients = Ingredient.objects.all()
#    #return render(request, 'rrs_app/recipe_search.html', {'all_ingredients':all_ingredients})
#    return render(request, 'rrs_app/recipe_search.html', {})


from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView


class RecipeListView(ListView):
    model = models.Recipe
    context_object_name = 'recipes'
    template_name = 'recipe_list.html' #default is also recipe_list.html

class RecipeDetailView(DetailView):
    model = models.Recipe
    context_object_name = 'recipe_details'
    template_name = 'recipe_detail.html' #default is also recipe_detail.html

class IngredientListView(ListView):
    model = models.Ingredient
    context_object_name = 'ingredients'
    template_name = 'recipe_search.html' #default is ingredient_list.html

class UserIngredientCreateView(CreateView):
    fields = ('ingredient','amount')
    model = models.UserIngredient

    def form_valid(self, form):

        if self.request.user.is_authenticated:
            #self.object = form.save(commit=False)
            form.instance.user = self.request.user
            #form.instance.ingredient = self.request.ingredient
            #form.instance.amount = self.request.amount
            #self.object.save()


        else: #buraya guest'ler için user_id generate edilme ve pantry girişi ilave edilecek
            pass

        return super().form_valid(form)

        #form.instance.user = self.request.user
        #UserIngredient.objects.update_or_create(user=self.request.user, ingredient=self.request.ingredient, amount=self.request.ingredient)


    def get_success_url(self):
        #return reverse_lazy('pantry_create')
        if self.request.POST.get('submit'):
            return reverse_lazy('pantry_create')
        elif self.request.POST.get('continue'):
            return reverse_lazy('recipe_list')


'''
class RecipeIngredientListView(ListView):
    model = models.RecipeIngredient
    context_object_name = 'recipes'
    template_name = 'recipe_list.html' #default is also recipe_list.html
'''
