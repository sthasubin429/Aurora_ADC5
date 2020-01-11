from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='aurora-main'),
   
    path('contactus/', views.contactus, name='aurora-contact'),

    path('aboutus/', views.aboutus, name='aurora-about'),
]

