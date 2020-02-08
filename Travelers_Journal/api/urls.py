from django.contrib import admin
from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    path('read/', views.read_api, name="read_api"),
    path('read/<int:ID>', views.read_api_data, name="read_api_data"),
    path('read/user/<int:ID>', views.read_api_user, name="read_api_user"),
    path('create/', views.create_api, name='create_api'),
    path('update/<int:ID>', views.update_api, name='update_api'),
    path('delete/<int:ID>', views.delete_api, name='delete_api'),
]
