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
    post_images = models.ImageField(default='post_images/default.jpg', upload_to='post_images')
    post_date = models.DateTimeField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title
'''
This is a data base to store all the ratings given to post and comments along with the post and comments along with the time the comments were done
Table as one to many relation with post table as one post can have multiple reactions but one reaction is associated with only one post.
Table also has one to many relation with user table as one user can make multiple reaction but only one user for any given reaction
This has on delete cascade as if user or post is deleted all the reaction associated with this is also deleted
'''

class React(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.username)

'''
This table is to keep track of the other users that any given user follows.
'''
class Follow(models.Model):
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed_by = models.TextField()
    time = models.DateTimeField()
    def __str__(self):
        return str(self.subscribed_to)
