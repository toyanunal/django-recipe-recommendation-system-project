from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Recipe, Ingredient, RecipeIngredient, UserIngredient, UserInfo
from .forms import SignUpForm, EditProfileForm, MyPasswordChangeForm
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
            messages.success(request,('Successfully logged in.'))
            return redirect('home') #routes to 'home' on successful login
        else:
            messages.error(request,('Username or password is wrong!'))
            return redirect('login') #re routes to login page upon unsucessful login
    else:
        return render(request, 'rrs_app/login.html', {})

def logout_user(request):
    logout(request)
    messages.warning(request,('Successfully logged out.'))
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
            messages.success(request, ('Successfully registered.'))
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
            messages.success(request, ('Profile successfully edited.'))
            return redirect('home')
    else:         #passes in user information
        form = EditProfileForm(instance= request.user)

    context = {'form': form}
    return render(request, 'rrs_app/edit_profile.html', context)

def change_password(request):
    if request.method =='POST':
        form = MyPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('Password successfully edited.'))
            return redirect('home')
    else:         #passes in user information
        form = MyPasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'rrs_app/change_password.html', context)

def faq(request):
    return render(request, 'rrs_app/faq.html', {})


def input_form_view(request):
    form = forms.InputForm()

    if not request.user.is_authenticated:
        messages.warning(request, ('Please login to continue.'))
        return redirect('home')

    if request.method == 'POST':
        form = forms.InputForm(request.POST)

        if form.is_valid():

            if form.cleaned_data['portion'] == '0':
                messages.warning(request,('Please choose a portion size.'))
                return render(request, 'rrs_app/input_form.html', {'form':form})

            try: #if this user has existing addcost and portion:
                ui = UserInfo.objects.get(user=request.user)
                ui.addcost = form.cleaned_data['addcost']
                ui.portion = form.cleaned_data['portion']
                ui.save()
            except: #if this user is new to the DB:
                ui = UserInfo(user=request.user, addcost=form.cleaned_data['addcost'], portion=form.cleaned_data['portion'])
                ui.save()

            form = forms.UserIngredientForm()
            messages.success(request,('The inputs are successfully recorded.'))
            return redirect('pantry_create')

        else:
            messages.warning(request,('The additional cost can be between 0 and 1,000,000!'))
            return render(request, 'rrs_app/input_form.html', {'form':form})

    return render(request, 'rrs_app/input_form.html', {'form':form})


def useringredient_form_view(request):
    form = forms.UserIngredientForm()

    if not request.user.is_authenticated:
        messages.warning(request, ('Please login to continue.'))
        return redirect('home')

    ingredient_list = []
    for i in Ingredient.objects.all():
        try:
            ingredient_object = UserIngredient.objects.get(user=request.user, ingredient=i)
            ingredient_list.append(ingredient_object)
        except:
            pass

    if request.method == 'POST':
        form = forms.UserIngredientForm(request.POST)

        if form.is_valid():
            ingredient_list = []
            for i in Ingredient.objects.all():
                try:
                    ingredient_object = UserIngredient.objects.get(user=request.user, ingredient=i)
                    ingredient_list.append(ingredient_object)
                except:
                    pass

            if 'complete' in request.POST:
                ###TAYLAN'ın kısım
                print(ingredient_list)






                messages.success(request,('Matching recipes are listed.'))
                return redirect('recipe_list')

            elif 'add' in request.POST and (form.cleaned_data['ingredient'] is None or form.cleaned_data['amount'] is None):
                messages.warning(request,('Both ingredient and amount fields need to be filled!'))
                return render(request, 'rrs_app/useringredient_form.html', {'form':form, 'ingredient_list':ingredient_list})

            try: #if this user-ingredient combination exists:
                ui = UserIngredient.objects.get(user=request.user, ingredient=form.cleaned_data['ingredient'])
                ui.amount = form.cleaned_data['amount']
                ui.save()
                messages.success(request,('The ingredient\'s amount is successfully updated.'))
            except: #if this user-ingredient combination is new to the DB:
                ui = UserIngredient(user=request.user, ingredient=form.cleaned_data['ingredient'], amount=form.cleaned_data['amount'])
                ui.save()
                messages.success(request,('The ingredient is successfully added to your pantry.'))

            form = forms.UserIngredientForm()

            if 'add' in request.POST:
                ingredient_list = []
                for i in Ingredient.objects.all():
                    try:
                        ingredient_object = UserIngredient.objects.get(user=request.user, ingredient=i)
                        ingredient_list.append(ingredient_object)
                    except:
                        pass

                return render(request, 'rrs_app/useringredient_form.html', {'form':form, 'ingredient_list':ingredient_list})

        else:
            messages.warning(request,('The amount can be between 0 and 1,000,000!'))
            return render(request, 'rrs_app/useringredient_form.html', {'form':form, 'ingredient_list':ingredient_list})

    return render(request, 'rrs_app/useringredient_form.html', {'form':form, 'ingredient_list':ingredient_list})


from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,DeleteView

def recipe_form_view(request):
    pass

class RecipeListView(ListView):
    model = models.Recipe
    context_object_name = 'recipes'
    template_name = 'recipe_list.html' #default is also recipe_list.html

class RecipeDetailView(DetailView):
    model = models.Recipe
    context_object_name = 'recipe_details'
    template_name = 'recipe_detail.html' #default is recipe_detail.html

class IngredientListView(ListView):
    model = models.Ingredient
    context_object_name = 'ingredients'
    template_name = 'recipe_search.html' #default is ingredient_list.html

class UserIngredientCreateView(CreateView):
    fields = ('ingredient','amount')
    model = models.UserIngredient
    context_object_name = 'user_ingredients'

    def form_valid(self, form):

        if self.request.user.is_authenticated:
            #self.object = form.save(commit=False)
            form.instance.user = self.request.user
            #form.instance.ingredient = self.request.ingredient
            #form.instance.amount = self.request.amount
            #self.object.save()
            #UserIngredient.objects.update_or_create(user=self.request.user, ingredient=self.request.ingredient, amount=self.request.ingredient)

            #UserIngredient.objects.raw('SELECT * FROM rrs_app_useringredient WHERE user="toyanunal"')
            #user=self.request.user, ingredient=self.request.ingredient, amount=self.request.ingredient


        else: #buraya guest'ler için user_id generate edilme ve pantry girişi ilave edilecek
            pass

        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('submit'):
            return reverse_lazy('pantry_create')
        elif self.request.POST.get('continue'):
            return reverse_lazy('recipe_list')
