from django.contrib import admin
from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    path('posts/read/', views.read_api, name="read_api"),
    path('posts/read/pagination/<int:SIZE>/<int:PAGENO>', views.read_api_pagination, name="read_api_pagination"),
    path('posts/read/<int:ID>', views.read_api_data, name="read_api_data"),
    path('posts/read/user/<int:ID>', views.read_api_user, name="read_api_user"),
    path('posts/create/', views.create_api, name='create_api'),
    path('posts/update/<int:ID>', views.update_api, name='update_api'),
    path('posts/delete/<int:ID>', views.delete_api, name='delete_api'),
]

'''
Api's URL pattern uses slug to process the request made through api

'''