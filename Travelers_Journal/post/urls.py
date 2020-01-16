from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path('', homePage),
    path('create/', create, name="create"),
    path('view/<int:ID>', viewPost),
    path('edit/<int:ID>', editPostUpdateForm),
    path('delete/<int:ID>', postDelete),
]
