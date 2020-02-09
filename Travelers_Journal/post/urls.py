from django.contrib import admin
from django.urls import path
from . import views
app_name = 'post'

urlpatterns = [
    path('', views.base, name='base'),
    path('<int:SIZE>/<int:PAGENO>', views.homePage, name='homePage'),
    path('create/', views.create, name="create"),
    path('view/<int:ID>', views.viewPost, name='viewPost'),
    path('edit/<int:ID>', views.editPostUpdateForm, name='update'),
    path('delete/<int:ID>', views.postDelete, name='delete'),
    path('followed/<str:USER>', views.followed, name='followed' )
]
