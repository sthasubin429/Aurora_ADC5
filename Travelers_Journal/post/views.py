from django.shortcuts import render,redirect
from .models import Posts
import datetime
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model as user_data
from django.db.models import Q

# Create your views here.
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
        
def homePage(request):
    post = Posts.objects.all()
    query = ""
    if request.GET:
        query = request.GET['searchKey']
    post = search(str(query))
    return render(request, 'post/index.html', context={'posts': post})


def create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('form Saved')
            return redirect('post:homepage')
    return render(request, 'post/create.html', {'form': form})


def viewPost(request, ID):
    postObj = Posts.objects.get(id=ID)
    context_varible = {
        'posts': postObj
    }
    return render(request, 'post/view.html', context_varible)


def editPostUpdateForm(request, ID):
    if request.method == "POST":
        postObj = Posts.objects.get(id=ID)
        postObj.post_title = request.POST['title']
        postObj.post_content = request.POST['content']
        postObj.post_date = datetime.datetime.now()
        postObj.save()
        return HttpResponse("Record Updated!! <br> <a href='/post'> Return to View</a>")
    postObj = Posts.objects.get(id=ID)
    context_varible = {
        'posts': postObj
    }
    return render(request, 'post/edit.html', context_varible)


def postDelete(request,ID):
    delPost = Posts.objects.get(id=ID)
    delPost.delete()
    return HttpResponse("Post Deleted!! <br> <a href='/post'> Return to View</a>")