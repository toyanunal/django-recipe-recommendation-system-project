from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib import messages
from . import models
from . import forms
from .models import Recipe, Ingredient, RecipeIngredient, UserIngredient, UserInfo
from .forms import SignUpForm, EditProfileForm, MyPasswordChangeForm, UserIngredientForm, RecipeForm
from django.contrib.auth.models import User


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
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('Profile successfully edited.'))
            return redirect('home')
    else:         #passes in user information
        if len(str(request.user)) >= 32:
            form = EditProfileForm()
            messages.error(request, ('Guests cannot edit profile info!'))
            return redirect('input_form')
        form = EditProfileForm(instance=request.user)

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
        if not request.session.exists(request.session.session_key):
            request.session.create()
        request.user = request.session.session_key
        try:
            user = User.objects.create_user(username=request.user,email=request.user+'@anonymous.com',password=request.user)
        except:
            user = User.objects.get(username=request.user)
        login(request,user)
        messages.warning(request, ('Proceeding with a guest user.'))

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
        messages.warning(request, ('Redirecting to the home page!'))
        return redirect('home')

    ingredient_list = UserIngredient.objects.filter(user=request.user)

    if request.method == 'POST':
        form = forms.UserIngredientForm(request.POST)

        if form.is_valid():
            ingredient_list = UserIngredient.objects.filter(user=request.user)

            if 'complete' in request.POST:
                messages.success(request,('Matching recipes are listed below.'))
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
                ingredient_list = UserIngredient.objects.filter(user=request.user)
                return render(request, 'rrs_app/useringredient_form.html', {'form':form, 'ingredient_list':ingredient_list})

        else:
            messages.warning(request,('The amount can be between 0 and 1,000,000!'))
            return render(request, 'rrs_app/useringredient_form.html', {'form':form, 'ingredient_list':ingredient_list})

    return render(request, 'rrs_app/useringredient_form.html', {'form':form, 'ingredient_list':ingredient_list})


def recipe_form_view(request):
    form = forms.RecipeForm()

    if not request.user.is_authenticated:
        messages.warning(request, ('Redirecting to the home page!'))
        return redirect('home')

    recipe_list = []
    inf = UserInfo.objects.get(user=request.user)

    for rec in Recipe.objects.all():
        total_diff = 0

        for rec_item in RecipeIngredient.objects.filter(recipe=rec):
            ing = Ingredient.objects.get(title=rec_item.ingredient)

            try:
                user_item = UserIngredient.objects.get(user=request.user, ingredient=rec_item.ingredient)
                amount_diff = rec_item.amount * inf.portion - user_item.amount
                #print("Try. rec: {} rec_item: {} rec_item.amount: {} inf.portion: {} user_item.amount: {} amount_diff: {}".format(rec, rec_item, rec_item.amount, inf.portion, user_item.amount, amount_diff))
            except:
                amount_diff = rec_item.amount * inf.portion
                #print("Except. rec: {} rec_item: {} rec_item.amount: {} inf.portion: {} user_item.amount: NONE amount_diff: {}".format(rec, rec_item, rec_item.amount, inf.portion, amount_diff))

            if amount_diff > 0:
                if ing.unit_type != 'count':
                    total_diff += amount_diff * ing.unit_cost / 1000
                else:
                    total_diff += amount_diff * ing.unit_cost
                #print("Total diff of {} increased to {}".format(rec, total_diff))

        if total_diff <= inf.addcost: #rec_item.add_cost <= inf.addcost:
            #print("Since total_diff {} is SMALLER than inf.addcost {} rec {} is ADDED to the list".format(total_diff, inf.addcost, rec))
            rec.total_cost = total_diff
            recipe_list.append(rec)
        recipe_list.sort(key=lambda x: x.total_cost)

    if request.method == 'POST':
        form = forms.RecipeForm(request.POST)

        if form.is_valid():
            if 'filter' in request.POST:
                if form.cleaned_data['meal_type'] is not None:
                    recipe_list = [recipe for recipe in recipe_list if recipe.meal_type == form.cleaned_data['meal_type']]

                if form.cleaned_data['diet_type'] is not None:
                    recipe_list = [recipe for recipe in recipe_list if recipe.diet_type == form.cleaned_data['diet_type']]

                if form.cleaned_data['effort'] is not None:
                    recipe_list = [recipe for recipe in recipe_list if recipe.effort == form.cleaned_data['effort']]

            elif 'reset' in request.POST:
                form = forms.RecipeForm()
                return render(request, 'rrs_app/recipe_list.html', {'form':form, 'recipe_list':recipe_list})

    return render(request, 'rrs_app/recipe_list.html', {'form':form, 'recipe_list':recipe_list})


def recipe_detail_view(request, slug):

    if not request.user.is_authenticated:
        messages.warning(request, ('Redirecting to the home page!'))
        return redirect('home')

    rec = Recipe.objects.get(slug=slug)
    inf = UserInfo.objects.get(user=request.user)
    recipe_list = []
    ingredient_list = []
    for rec_item in RecipeIngredient.objects.filter(recipe=rec):
        ing = Ingredient.objects.get(title=rec_item.ingredient)
        recipe_list.append(rec_item)

        try:
            user_item = UserIngredient.objects.get(user=request.user, ingredient=rec_item.ingredient)
            amount_diff = rec_item.amount * inf.portion - user_item.amount

            if amount_diff > 0:
                user_item.amount = amount_diff
                if ing.unit_type != 'count':
                    user_item.total_cost = ing.unit_cost * user_item.amount / 1000
                else:
                    user_item.total_cost = ing.unit_cost * user_item.amount
            else:
                user_item.amount = "-"
                user_item.total_cost = "-"
            ingredient_list.append(user_item)

        except:
            rec_item.amount = rec_item.amount * inf.portion
            if ing.unit_type != 'count':
                rec_item.total_cost = ing.unit_cost * rec_item.amount / 1000
            else:
                rec_item.total_cost = ing.unit_cost * rec_item.amount
            ingredient_list.append(rec_item)

    ingredient_list = list(zip(recipe_list, ingredient_list))

    if 'completed' in request.POST and request.POST.getlist("check") == ['on']:
        for rec_item in RecipeIngredient.objects.filter(recipe=rec):
            ing = Ingredient.objects.get(title=rec_item.ingredient)

            try:
                user_item = UserIngredient.objects.get(user=request.user, ingredient=rec_item.ingredient)
                amount_diff = rec_item.amount * inf.portion - user_item.amount

                if amount_diff > 0:
                    user_item.amount = 0
                    user_item.save()

                else:
                    user_item.amount = user_item.amount - rec_item.amount * inf.portion
                    user_item.save()

            except:
                pass

        messages.warning(request,('Given amounts of the ingredients are subtracted from your pantry!'))
        return redirect('recipe_detail', slug=slug)

    return render(request, 'rrs_app/recipe_detail.html', {'recipe_details':rec, 'ingredient_list':ingredient_list})
