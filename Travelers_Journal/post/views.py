from django.shortcuts import render,redirect,get_object_or_404
from .models import Posts, React, Follow
import datetime
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model as user_data
from django.db.models import Q
from django.db.models import Avg
from math import ceil
# Create your views here.


#Logic for view funciton
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
def base(request):
    return redirect('/post/5/1')
'''
View function that renders the main post page.this function initialy queries the database and returns all the posts stored in the database
if the user is searches a post, it quereies tha database and returns only the post matched with the search querry
'''
def homePage(request,SIZE,PAGENO):
    skip = SIZE * (PAGENO - 1)
    post = Posts.objects.all().order_by('-post_date')[skip: (PAGENO * SIZE)]
    noOfPages = int(ceil(Posts.objects.all().count()/SIZE))
    query = ""
    if request.GET:
        query = request.GET['searchKey']
        post = search(str(query))
        return render(request, 'post/index.html', {'posts': post})
    return render(request, 'post/index.html', {'posts': post, 'noOfPages': range(1,noOfPages+1)})

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
            print('form Saved')
            return redirect('/')
    elif request.user.is_authenticated:
        return render(request, 'post/create.html', {'form': form})
    else:
        return HttpResponse("Please Login <br> <a href='/post'> Return to View</a> <br> <a href='/login'> Login </a>")



'''
Simple view function to display any particular post.
This function users slug to determine which post the user asked to display and only displays the post asked by the user.
'''
def viewPost(request, ID):
    postObj = Posts.objects.get(id=ID)
    ratingObj = React.objects.filter(post_id=ID).aggregate((Avg('rating')))
    commentObj = React.objects.filter(post_id=ID)
    print(ratingObj)
    if ratingObj['rating__avg'] is None:
        ratingObj = 'None'
    else:
        ratingObj = round(ratingObj['rating__avg'],2)
    if request.method == 'POST' and request.user.is_authenticated:
        get_rating = request.POST['rating']
        get_comment = request.POST['comment']
        react_obj = React(post_id=postObj, username=request.user,rating=get_rating, comment=get_comment, time=datetime.datetime.now())
        react_obj.save()
        return render(request, 'post/view.html', {'posts': postObj, 'rating': ratingObj, 'comments': commentObj})

    elif not request.user.is_authenticated and request.method == 'POST':
        return HttpResponse("Please Login <br> <a href='/post'> Return to View</a> <br> <a href='/login'> Login </a>")
    return render(request, 'post/view.html', {'posts': postObj, 'rating': ratingObj, 'comments': commentObj})

def followed(request, USER):
    followObj = Follow.objects.filter(subscribed_by=USER)
    userset = []
    for f in followObj:
        userset.append(f.subscribed_to)
    postObj = Posts.objects.filter(username__in=userset)
    return render(request, 'post/follow.html', {'posts':postObj})

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
            return HttpResponse("post updated <a href='/post'> Return to View</a>")
    elif request.user == inst.username:
        return render(request, "post/edit.html", {"form": form, "posts": inst})
    elif request.user.is_authenticated:
        return HttpResponse("You cannot edit this post as you are not the orginal creator of this post <br> <a href='/post'> Return to View</a>")
    else:
        return HttpResponse("Please Login <br> <a href='/post'> Return to View</a> <br> <a href='/login'> Login </a>")


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
        return HttpResponse("Post Deleted!! <br> <a href='/post'> Return to View</a>")
    elif request.user.is_authenticated:
        return HttpResponse("You cannot delete this post as you are not the orginal creator of this post <br> <a href='/post'> Return to View</a>")
    else:
        return HttpResponse("Please Login <br> <a href='/post'> Return to View</a> <br> <a href='/login'> Login </a>")
