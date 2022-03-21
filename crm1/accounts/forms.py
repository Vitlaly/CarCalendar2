from django.forms import ModelForm
from .models import Component, Owner
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = '__all__'
        exclude = ['owner']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'
        exclude = ['user', 'name']


