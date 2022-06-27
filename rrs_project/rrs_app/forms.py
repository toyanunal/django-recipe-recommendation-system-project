from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms


class EditProfileForm(UserChangeForm):
    password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))

    class Meta:
        model = User
        fields = ('username', 'email','password',)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['email'].label = ''


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'
        self.fields['old_password'].label = ''

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same new password, for verification.</small></span>'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['email'].label = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Ingredient, UserIngredient, UserInfo, Recipe

PORTION_CHOICES = (
    (0, 'Portion size'),
    (1, '1'),
    (0.5, '½'),
    (0.25, '¼'),
)

class InputForm(forms.ModelForm):
    addcost = forms.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000000)], label='Enter additional cost:')
    portion = forms.ChoiceField(choices=PORTION_CHOICES, label='Enter portion size:')

    class Meta:
        model = UserInfo
        fields = ('addcost', 'portion')

    def clean(self):
        all_clean_data = super().clean()

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)

        self.fields['addcost'].widget.attrs['class'] = 'form-control'
        self.fields['addcost'].widget.attrs['placeholder'] = 'Additional money to spent'
        self.fields['addcost'].label = ''
        self.fields['addcost'].help_text = '<span class="form-text text-muted"><small>Required. Enter how much Turkish Liras (₺) you are willing to spend.</small></span>'

        self.fields['portion'].widget.attrs['class'] = 'form-control'
        self.fields['portion'].widget.attrs['placeholder'] = 'Portion size'
        self.fields['portion'].label = ''
        self.fields['portion'].help_text = '<span class="form-text text-muted"><small>Required. Choose portion size based on the number of people.</span><ul class="form-text text-muted"><li>Portion size 1 is for 4 people.</li><li>Portion size ½ is for 2 people.</li><li>Portion size ¼ is for 1 people.</ul>'


class UserIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(empty_label="Ingredient", required=False, queryset=Ingredient.objects.all(), label='Select ingredient:')
    amount = forms.FloatField(required=False, validators=[MinValueValidator(0), MaxValueValidator(1000000)], label='Enter amount:')

    class Meta:
        model = UserIngredient
        fields = ('ingredient', 'amount')

    def clean(self):
        all_clean_data = super().clean()

    def __init__(self, *args, **kwargs):
        super(UserIngredientForm, self).__init__(*args, **kwargs)

        self.fields['ingredient'].widget.attrs['class'] = 'form-control'
        self.fields['ingredient'].widget.attrs['placeholder'] = 'Ingredient'
        self.fields['ingredient'].label = ''
        self.fields['ingredient'].help_text = '<span class="form-text text-muted"><small>Required. Add ingredients that are present in your fridge and pantry.</small></span>'

        self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['amount'].widget.attrs['placeholder'] = 'Amount'
        self.fields['amount'].label = ''
        self.fields['amount'].help_text = '<span class="form-text text-muted"><small>Required. Enter the amount you have for the selected ingredient.</span><ul class="form-text text-muted"> \
        <li>Amount is based on pieces (pcs) for the following ingredients: Egg, Garlic, Parsley, Rosemary, Scallion and Zucchini.</li> \
        <li>Amount is based on milliliters (ml) for the following ingredients: Cream, Milk, Olive oil, Sunflower oil.</li> \
        <li>Amount is based on grams (gr) for all the remaining ingredients.</ul>'


class RecipeForm(forms.ModelForm):
    meal_type = forms.ModelChoiceField(empty_label="Meal type", required=False, queryset=Recipe.objects.values_list('meal_type', flat=True).distinct().order_by('meal_type'), to_field_name='meal_type')
    diet_type = forms.ModelChoiceField(empty_label="Diet type", required=False, queryset=Recipe.objects.values_list('diet_type', flat=True).distinct().order_by('diet_type'), to_field_name='diet_type')
    effort = forms.ModelChoiceField(empty_label="Effort", required=False, queryset=Recipe.objects.values_list('effort', flat=True).distinct().order_by('effort'), to_field_name='effort')

    class Meta:
        model = Recipe
        fields = ('meal_type', 'diet_type', 'effort')

    def clean(self):
        all_clean_data = super().clean()

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        self.fields['meal_type'].widget.attrs['class'] = 'form-control'
        self.fields['meal_type'].widget.attrs['placeholder'] = 'Meal type'
        self.fields['meal_type'].label = ''
        self.fields['meal_type'].help_text = '<span class="form-text text-muted"><small>Not required. Filter recipes based on their meal types.</small></span>'

        self.fields['diet_type'].widget.attrs['class'] = 'form-control'
        self.fields['diet_type'].widget.attrs['placeholder'] = 'Diet type'
        self.fields['diet_type'].label = ''
        self.fields['diet_type'].help_text = '<span class="form-text text-muted"><small>Not required. Filter recipes based on their diet types.</small></span>'

        self.fields['effort'].widget.attrs['class'] = 'form-control'
        self.fields['effort'].widget.attrs['placeholder'] = 'Effort'
        self.fields['effort'].label = ''
        self.fields['effort'].help_text = '<span class="form-text text-muted"><small>Not required. Filter recipes based on the effort required.</small></span>'
