from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.

register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST) 
		if form.is_valid():
			user = form.save() 
			login(request, user) 
			return redirect('main:homepage') 



	form = UserCreationForm()
	return render(request, "login/login.html", context={"form":form})
