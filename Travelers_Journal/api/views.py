from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from post.models import Posts
from django.contrib.auth.models import User
import json
import datetime
# Create your views here.

def read_api(request):
    post = Posts.objects.all()
    dict_value = {"posts": list(post.values('post_title', 'post_content', 'post_date', 'username'))}
    return JsonResponse(dict_value)


def read_api_data(request, ID):
    post = Posts.objects.get(id=ID)
    return JsonResponse({"post_title": post.post_title, "post_content": post.post_content})


def read_api_user(request, ID):
    post = Posts.objects.filter(username=ID)
    dict_value = {"posts": list(post.values('post_title', 'post_content', 'post_date', 'username'))}
    return JsonResponse(dict_value)

@csrf_exempt
def create_api(request):
    decoded_data = request.body.decode('utf-8')
    post_data = json.loads(decoded_data)
    title = post_data['title']
    content = post_data['content']
    username = [post_data['username']]
    user = User.objects.get(username__in=username)
    print(user)
    post = Posts(post_title=title, post_content=content, post_date=datetime.datetime.now(), username=user)
    post.save()
    return JsonResponse({"message": "Post Sucessfully Created!!!"})

@csrf_exempt
def update_api(request, ID):
    post = Posts.objects.get(id=ID)
    if request.method == 'GET':
        return JsonResponse({"post_title": post.post_title, "post_content": post.post_content})
    decoded_data = request.body.decode('utf-8')
    post_data = json.loads(decoded_data)
    post.post_title = post_data['title']
    post.post_content = post_data['content']
    post_date = datetime.datetime.now()
    post.save()
    return JsonResponse({"message": "Successfully updated!!"})

@csrf_exempt 
def delete_api(request, ID):
    post = Posts.objects.get(id=ID)
    post.delete()
    return JsonResponse({"message": "Post Deleted"})
