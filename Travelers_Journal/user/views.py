from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.s

#post that renders base template
#this function redirets to the page where user can view all the post
def base(request):
    return redirect('/post')

'''
View function that registers any new user

'''
def register(request):
    if request.method == 'POST':
        print(request.method)
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            user = User.objects.create_user(
                username=username, password=password1, email=email)
            user.save()
        user = authenticate(username=username, password=password1)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('user:base')
    else:
        return render(request, 'user/register.html')


'''
View function that logs in already exesting user

'''
def signin(request):
    if request.method == 'POST':
        print(request.method)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('user:base')

    return render(request, 'user/login.html')

#view funstion to signout and kill the curent session
def signout(request):
    logout(request)
    return render(request, 'user/logout.html')

#view funstion that shows the current user profile
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'user/profile.html')
    else:
        return redirect('user:login')
