from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import DateInput

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(widget=forms.PasswordInput,label="Contraseña")

    

