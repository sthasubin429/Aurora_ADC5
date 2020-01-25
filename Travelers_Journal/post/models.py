from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.

'''
This is our main database Posts.
This stores all the data base of our posts.
This table has an attribute username that is the foreign key and links with the use tabe
This shows a one to many relation between user and post table as one user can create mutiple posts and also one post can have only one user as its creater.
This has on_delete cascade as once the user deletes his or her profile all the posts created by the user is also automatically deleted
'''
class Posts(models.Model):
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_images = models.ImageField(default='default.jpg', upload_to='post_images')
    post_date = models.DateTimeField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title
