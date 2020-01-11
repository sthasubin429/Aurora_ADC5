from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from  .forms import CustomForm 


# Create your views here.

def register(request):
    form = CustomForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('register')       #change redirect path to homepage
        else:
            form = CustomForm()
    return render(request, 'user/register.html', {'form' : form})

def base(request):
    return render(request, 'users/base.html')