from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from  .forms import CustomForm 
from django.contrib.auth import login, logout, authenticate


def register(request):
    if request.method == "POST":
        form = CustomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base')       #change redirect path to homepage
    else:
        form = CustomForm()
    return render(request, 'user/register.html', {'form' : form})

def base(request):
    return render(request, 'user/base.html')

