from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from todoapp.models import Todo, Profile

class UserRegisterForm(UserCreationForm):
    # category = forms.CharField(max_length=25)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['category']

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title','status','priority']