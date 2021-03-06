from django.shortcuts import render,redirect,get_object_or_404
from .models import Posts, React, Follow
import datetime
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model as user_data
from django.db.models import Q
from django.db.models import Avg
from math import ceil
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

# Create your views here.


'''Logic for view funciton'''
def search(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Posts.objects.filter(
            Q(post_title__icontains=q) |
            Q(post_content__icontains=q)
        )

        for post in posts:
            queryset.append(post)

    return list(set(queryset))

'''
redirects request to dispay data by implemending pagination
'''
def base(request):
    return redirect('/post/5/1')

'''
View function that renders the main post page.this function initialy queries the database and returns all the posts stored in the database
Data is returned in a paged format depending upon the size and page given.
it also calculates the maximum number of page required to display all the post and html files only displays the appropriate number of pages
Dynamically increases the number of pages as the number of posts increases
if the user is searches a post, it quereies tha database and returns only the post matched with the search querry
'''
def homePage(request,SIZE,PAGENO):

    skip = SIZE * (PAGENO - 1)
    post = Posts.objects.all().order_by('-post_date')[skip: (PAGENO * SIZE)]
    recentPost = Posts.objects.all().order_by('-post_date')[0:4]
    noOfPages = int(ceil(Posts.objects.all().count()/SIZE))
    userFirstLetter = str(request.user)[0].upper()
    if request.user.is_authenticated:
        followObj = Follow.objects.filter(subscribed_by=request.user.username)
    else:
        followObj = None
    if request.user.is_authenticated:
        postObj = Posts.objects.filter(username=request.user)
        postList = []
        for p in postObj:
            postList.append(p.id)
        notification = React.objects.filter(post_id__in=postList)
    else:
        postObj = None
        notification = None 
    query = ""
    if request.GET:
        query = request.GET['searchKey']
        post = search(str(query))
        return render(request, 'post/index.html', {'posts': post, 'followObj': followObj, 'recentPost': recentPost, 'userFLetter': userFirstLetter, 'notification': notification})
    return render(request, 'post/index.html', {'posts': post, 'noOfPages': range(1,noOfPages+1), 'followObj':followObj, 'recentPost':recentPost, 'userFLetter':userFirstLetter,'notification':notification})

'''
View function for creating a new fucntion.
We use forms.py to create a form.
This function requires user to be logged in before creating any post.
We have used instance property of form class to instanciate username and the current date and time.
This is done as we want our app to auto insert username and current time at the time of the creation of post and not allow user to edit these values
'''
def create(request):
    form = PostForm()
    if request.method == "POST" and request.user.is_authenticated:
        form = PostForm(request.POST, request.FILES)
        form.instance.username = request.user
        form.instance.post_date = datetime.datetime.now()
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Created!!')
            return redirect('post:base')
        else:
            messages.warning(request, 'Post Data not valid')
            return redirect('post:create')
    elif request.user.is_authenticated:
        return render(request, 'post/create.html', {'form': form})
    else:
        messages.warning(request, 'Please Login to Continue')
        return redirect('user:login')



'''
Simple view function to display any particular post.
This function users slug to determine which post the user asked to display and only displays the post asked by the user.
This view function also displays all the comments posted on this post and also dispays the average rating of the post.
If the user submits blank rating and comment ir relods the same page by expecting multi value dictionary error
Also if the user is not authenticated when submitting a rating and comment, it redirects to the login page.
'''
def viewPost(request, ID):
    postObj = Posts.objects.get(id=ID)
    recentPost = Posts.objects.all().order_by('-post_date')[0:4]
    ratingObj = React.objects.filter(post_id=ID).aggregate((Avg('rating')))
    commentObj = React.objects.filter(post_id=ID)
    print(ratingObj)
    if ratingObj['rating__avg'] is None:
        ratingObj = 'None'
    else:
        ratingObj = round(ratingObj['rating__avg'],2)
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            get_rating = request.POST['rating']
            get_comment = request.POST['comment']
            react_obj = React(post_id=postObj, username=request.user,rating=get_rating, comment=get_comment, time=datetime.datetime.now())
            react_obj.save()
            ratingObj = React.objects.filter(post_id=ID).aggregate((Avg('rating')))
            ratingObj = round(ratingObj['rating__avg'], 2)
            return render(request, 'post/view.html', {'posts': postObj, 'rating': ratingObj, 'comments': commentObj,'recentPost':recentPost})
        except MultiValueDictKeyError:
            return render(request, 'post/view.html', {'posts': postObj, 'rating': ratingObj, 'comments': commentObj,'recentPost':recentPost})
    elif not request.user.is_authenticated and request.method == 'POST':
        messages.warning(request, 'Please Login to Continue')
        return redirect('user:login')
    return render(request, 'post/view.html', {'posts': postObj, 'rating': ratingObj, 'comments': commentObj,'recentPost':recentPost})

'''
This method opens a page that shows the post from the users that the logged in user has followed.
If the user is not authenticated, it redirects to a login page with appropriate message
'''
def followed(request, USER):
    if request.user.is_authenticated:
        followObj = Follow.objects.filter(subscribed_by=USER)
        userFirstLetter = str(request.user)[0].upper()
        recentPost = Posts.objects.all().order_by('-post_date')[0:4]
        userset = []
        for f in followObj:
            userset.append(f.subscribed_to)
        postObj = Posts.objects.filter(username__in=userset)
        return render(request, 'post/follow.html', {'posts':postObj,'recentPost': recentPost,'userFLetter':userFirstLetter})
    else:
        messages.warning(request, 'Please Login to Continue')
        return redirect('user:login')
'''
View funtion to edit any post.
This function users slug to determine which post the user the user asked to edit and displays the post asked by the user.
This function also checks weather the user is logged in or not.
Only allows the user to edit any post if the user sending the request to edit this post is the orgninal creator of the post
'''
def editPostUpdateForm(request, ID):
    inst = get_object_or_404(Posts, id=ID)
    form = PostForm(instance=inst)
    form.instance.post_date = datetime.datetime.now()
    if request.method == "POST" and request.user == inst.username:
        form = PostForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Updated!!!')
            return redirect(f'/post/view/{ID}')
    elif request.user == inst.username:
        return render(request, "post/edit.html", {"form": form, "posts": inst})
    elif request.user.is_authenticated:
        messages.warning(request, 'You cannot edit this post as You are not the orginal creator of this post!!')
        return redirect(f'/post/view/{ID}')
    else:
        messages.warning(request, 'Please Login to Continue')
        return redirect('user:login')


'''
View funtion to delete.
This function users slug to determine which post the user the user asked to delete and displays the post asked by the user.
This function also checks weather the user is logged in or not.
Only deletes the post if the user sending the request to delete the post is the orginal creator of the post
'''
def postDelete(request, ID):
    delPost = Posts.objects.get(id=ID)
    if request.user == delPost.username:
        delPost.delete()
        messages.warning(request, 'Your Post has been Deleted!!')
        return redirect('user:profile')
    elif request.user.is_authenticated:
        messages.warning(request, 'You cannot delete this post as you are not the orginal creator of this post!!')
        return redirect(f'/post/view/{ID}')
    else:
        messages.warning(request, 'Please Login to Continue')
        return redirect('user:login')
 
