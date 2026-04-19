from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='First name', max_length=150)
    last_name = forms.CharField(label='Last name', max_length=150)
    username = forms.CharField(label='Username', help_text='')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='')
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, help_text='')
    is_owner = forms.BooleanField(required=False, label='Register as restaurant owner')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'is_owner']