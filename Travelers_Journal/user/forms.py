from django import forms
from django.contrib.auth.models import User

class CustomForm(UserCreationForm):

    email = forms.EmailField(required=True)
    
    class meta:
        model = User
        field = ['username', 'email', 'password1', 'password2']

