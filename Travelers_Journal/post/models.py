from django.db import models

# Create your models here.


class Posts(models.Model):
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_images = models.ImageField(default='default.jpg', upload_to='post_images')
    post_date = models.DateTimeField()

    def __str__(self):
        return self.post_title
