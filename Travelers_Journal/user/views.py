from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from post.models import Posts, React, Follow
from django.contrib import messages
import datetime
from django.db import IntegrityError

# Create your views here

'''#post that renders base template
#this function redirets to the page where user can view all the post'''
def base(request):
    return redirect('/post')

'''
View function that registers any new user
Checks if all the userinput data are valid then only creates a user 

'''
def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            if password1 == password2:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
            else:
                messages.warning( request, 'Password Did Not match')
                return render(request, 'user/register.html')
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, f'Account has been sucessfully created for {username}!')
                return redirect('user:profile')
        except IntegrityError:
            messages.warning(request, 'Username or Email already exists')
            return render(request, 'user/register.html')
    else:
        return render(request, 'user/register.html')


'''
View function that logs in already exesting user after checking if all the data entered are valid

'''
def signin(request):
    if request.user.is_authenticated:
        return redirect('user:profile')
    elif request.method == 'POST':
        print(request.method)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login sucessful')
            return redirect('post:base')
        else:
            messages.warning(request, 'Username or Password did not match!!!')
            return redirect('user:login')
    return render(request, 'user/login.html')

'''view funstion to signout and kill the curent session'''
def signout(request):
    logout(request)
    messages.warning(request, 'You have been Logged Out!!')
    return redirect('post:base')

'''
view funstion that shows the current user profile along with all the post created by the user
This function also creates a notification object from react table.
To create notification object, gets all the post id of the posts created by the user.
Then, using all the post id, gets all the entries made for the post id in the React table.
This is displayed as nottification in the html page

'''
def profile(request):
    if request.user.is_authenticated:
        postObj = Posts.objects.filter(username=request.user)
        postList = []
        for post in postObj:
            postList.append(post.id)
        notification = React.objects.filter(post_id__in=postList)
        followObj = Follow.objects.filter(subscribed_by=request.user.username)
        userFirstLetter = str(request.user)[0].upper()
        return render(request, 'user/profile.html', {'posts': postObj, 'notification':notification, 'followObj': followObj, 'userFLetter': userFirstLetter})
    else:
        return redirect('user:login')

'''
Function to view profile of any other user.
Displays all the posts uploaded by the user.
User must be logged in to view all the posts
Provides option to follow the user if not already followed.
If already followed does not provide an option to follow again
'''
def viewProfile(request, USER):
    if request.user.is_authenticated:
        recentPost = Posts.objects.all().order_by('-post_date')[0:4]
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
            messages.success(request, 'Subscribed')
            return redirect(f'/profile/{USER}')
        else:
            follow = False
            if not Follow.objects.filter(subscribed_by=request.user, subscribed_to=USER):
                follow = True
            postObj = Posts.objects.filter(username=USER).order_by('-post_date')
            return render(request, 'user/viewProfile.html', {'posts': postObj, 'follow': follow,'recentPost':recentPost})
    else:
        messages.warning(request, 'Please Login to Continue')
        return redirect('user:login')
