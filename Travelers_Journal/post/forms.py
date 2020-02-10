from django import forms
from .models import Posts

"""Form class for creating and editing the posts"""

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('post_title', 'post_content', 'post_images')