from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from post.models import Posts
from django.contrib.auth.models import User
import json
import datetime
from math import ceil
# Create your views here.
'''
This is the view function of rest API app.
'''

'''
This view function is used to return all the posts stored in our database in JSON format.
This function returns title of post, its content, its last modifided date along with the userid of the user that created this post.
'''
def read_api(request):
    post = Posts.objects.all()
    dict_value = {"posts": list(post.values('post_title', 'post_content', 'post_date', 'username'))}
    return JsonResponse(dict_value)

'''
This view function is used to return posts stored in our database by implemending pagination.
This view function uses slug in its url to got size and page number.
Depending upon the size and page no given it only returns required number of posts in JSON format.
'''
def read_api_pagination(request, SIZE, PAGENO):
    skip = SIZE * (PAGENO - 1)
    post = Posts.objects.all().order_by('-post_date')[skip: (PAGENO * SIZE)]
    noOfPages = int(ceil(Posts.objects.all().count() / SIZE))
    dict_value = {"posts": list(post.values('post_title', 'post_content', 'post_date', 'username'))}
    if PAGENO > noOfPages:
        return JsonResponse({"message": "This Page Contains no Data", "max_valid_page": noOfPages})
    return JsonResponse(dict_value)

'''
This view function returns only one post.
This view function uses slug to get post id and using the post id it gets the post and returns it in JSON format
'''
def read_api_data(request, ID):
    post = Posts.objects.get(id=ID)
    return JsonResponse({"post_title": post.post_title, "post_content": post.post_content})

'''
This view functions returns all the posts created by a particular user.
This view function uses slug to get user id and using the user id it filters all the post created by the user and returns it in JSON format.
'''
def read_api_user(request, ID):
    post = Posts.objects.filter(username=ID)
    dict_value = {"posts": list(post.values('post_title', 'post_content', 'post_date', 'username'))}
    return JsonResponse(dict_value)


'''
This view function is for creating a new post through api.
If url of this view function is opended in browser, it is redirected to create post page.
The api takes post request and body has title, content and username.
Username must be a valid username else it returns an error.
if username is valid it creats a new post with the given username, title and content.
Returns a suscessfull message after post is sucessfully created in json format
'''
@csrf_exempt
def create_api(request):
    if request.method == 'GET':
        return redirect('post:create')
    if request.method == 'POST':
        decoded_data = request.body.decode('utf-8')
        post_data = json.loads(decoded_data)
        title = post_data['title']
        content = post_data['content']
        username = [post_data['username']]
        user = User.objects.get(username__in=username)
        post = Posts(post_title=title, post_content=content, post_date=datetime.datetime.now(), username=user)
        post.save()
        return JsonResponse({"message": "Post Sucessfully Created!!!"})

'''
This view fuction is to update post stored in database.
This function uses slug to get the post id.
The api takes post request with title and content. 
This function gets the post and changes the title and content to the title and content in the request.
This function also updates the time on the post
Returns a sucessful message after update is completed
'''
@csrf_exempt
def update_api(request, ID):
    post = Posts.objects.get(id=ID)
    if request.method == 'GET':
        return JsonResponse({"post_title": post.post_title, "post_content": post.post_content})
    if request.method == 'POST':
        decoded_data = request.body.decode('utf-8')
        post_data = json.loads(decoded_data)
        post.post_title = post_data['title']
        post.post_content = post_data['content']
        post_date = datetime.datetime.now()
        post.save()
        return JsonResponse({"message": "Successfully updated!!"})

'''
This view function used to delete the post stored in data base.
This function uses slug to get post id.
Delets the post associated with the id and returns a message after the post has been deleted
'''
@csrf_exempt 
def delete_api(request, ID):
    if request.method == 'DELETE':
        post = Posts.objects.get(id=ID)
        post.delete()
        return JsonResponse({"message": "Post Deleted"})
