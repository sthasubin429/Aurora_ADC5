from django.contrib import admin

# Register your models here.
from .models import Posts
from .models import React
from .models import Follow

'''
Registerd all our classes from models to be accessed by admin
'''
admin.site.register(Posts)
admin.site.register(React)
admin.site.register(Follow)
