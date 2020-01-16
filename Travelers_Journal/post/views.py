from django.shortcuts import render
from .models import Posts
import datetime
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model as user_data


# Create your views here.
def search(request, key):
    #key = key.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    if key[0] == '@':
        key = key[1:]
        print(key)
    elif key == '' or not Posts.objects.filter(post_title__contains=key):
        return HttpResponse('Page Not Found123')
    else:
        return render(request, 'post/index.html', {'posts': Posts.objects.filter(post_title__contains=key)})
        
def homePage(request):
    if request.method == "POST":
        if request.POST['searchKey'] == '':
            return HttpResponse('Page Not Found')
        return search(request, request.POST['searchKey'])
    return render(request, 'post/index.html', context={'posts': Posts.objects.all})


def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        title = request.POST['title']
        content = request.POST['content']
        image = request.POST['image']
        date = datetime.datetime.now()
        post = Posts(post_title=title, post_content=content,
                        post_images=image, post_date=date)
        post.save()
        print("post Saved")
        return render(request, 'post/index.html', context={'posts': Posts.objects.all})
    form = PostForm()
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
    delPost = Posts.objects.filter(id=ID)
    delPost.delete()
    return HttpResponse("Post Deleted!! <br> <a href='/post'> Return to View</a>")