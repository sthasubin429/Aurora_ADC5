from django.shortcuts import render
from .models import Posts
import datetime
from .forms import PostForm
from django.http import HttpResponse


# Create your views here.

def homePage(request):
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
