from django.test import TestCase

# Create your tests here.
from post.models import Posts
from datetime import datetime


class OrmTest(TestCase):
    def setUp(self):
        Posts.objects.create(post_title="Test Title", post_content="Test Content", post_date=datetime.now())
        Posts.objects.create(post_title="Test Title1", post_content="Test Content1", post_date=datetime.now())
        Posts.objects.create(post_title="Test Title2", post_content="Test Content2", post_date=datetime.now())
        Posts.objects.create(post_title="Test Title3", post_content="Test Content4  ", post_date=datetime.now())
        
        
    def testORM(self):
        testPostObj = Posts.objects.get(post_title="Test Title")
        testPostObj1 = Posts.objects.get(post_title="Test Title1")
        
        self.assertEqual(testPostObj.post_title, "Test Title")
        self.assertEqual(testPostObj.post_content, "Test Content")
        self.assertIsNot(testPostObj.id, testPostObj1.id)
        self.assertIsNotNone(testPostObj)
