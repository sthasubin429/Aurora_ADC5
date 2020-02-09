from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from post.models import Posts, React, Follow
import datetime
from django.db import IntegrityError

# Create your views here
#post that renders base template
#this function redirets to the page where user can view all the post
def base(request):
    return redirect('/post')

'''
View function that registers any new user

'''
def register(request):
    if request.method == 'POST':
        try:
            print(request.method)
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            if password1 == password2:
                user = User.objects.create_user(
                    username=username, password=password1, email=email)
                user.save()
            else:
                return render(request, 'user/register.html')
            user = authenticate(username=username, password=password1)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('user:base')
        except IntegrityError:
            return render(request, 'user/register.html')
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
        postObj = Posts.objects.filter(username=request.user)
        postList = []
        for post in postObj:
            postList.append(post.id)
        notification = React.objects.filter(post_id__in=postList)
        return render(request, 'user/profile.html', {'posts': postObj, 'notification':notification})
    else:
        return redirect('user:login')

def viewProfile(request, USER):
    if request.user.is_authenticated:
        inst = Posts.objects.filter(username=USER)
        if not inst:
            return HttpResponse(status=404)
        for i in inst:
            inst = i
            break
        if request.user == inst.username:
            return redirect('user:profile')
        elif request.method == 'POST':
            subscribed_by = request.user
            subscribed_to = inst.username
            follow_obj = Follow(subscribed_to=subscribed_to,subscribed_by=subscribed_by, time=datetime.datetime.now())
            follow_obj.save()
            return render(request, 'user/subscribed.html')
        else:
            follow = False
            if not Follow.objects.filter(subscribed_by=request.user, subscribed_to=USER):
                follow = True
            postObj = Posts.objects.filter(username=USER).order_by('-post_date')
            return render(request, 'user/viewProfile.html', {'posts': postObj, 'follow': follow})
    else:
        return redirect('user:login')
