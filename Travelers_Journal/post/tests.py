from django.test import TestCase

# Create your tests here.
from post.models import Posts
from datetime import datetime


class OrmBasicTest(TestCase):
    def setUp(self):
        Posts.objects.create(post_title="Test Title", post_content="Test Content", post_date=datetime.now())
        Posts.objects.create(post_title="Test Title1", post_content="Test Content1", post_date=datetime.now())
        Posts.objects.create(post_title="Test Title2", post_content="Test Content2", post_date=datetime.now())
        
    def testORM(self):
        testPostObj = Posts.objects.get(post_title="Test Title")
        testPostObj1 = Posts.objects.get(post_title="Test Title1")
        
        self.assertEqual(testPostObj.post_title, "Test Title")
        self.assertEqual(testPostObj.post_content, "Test Content")
        self.assertIsNot(testPostObj.id, testPostObj1.id)
        self.assertIsNotNone(testPostObj)

class OrmUpdateTest(TestCase):
    def setUp(self):
        Posts.objects.create(post_title="Test Title", post_content="Test Content", post_date=datetime.now())

    def testORM(self):
        testPostObj = Posts.objects.get(post_title="Test Title")
        testPostObj.post_title = "Updated Title"
        testPostObj.post_content = "Updated Content"
        testPostObj.save()
        self.assertEqual(testPostObj.post_title, "Updated Title")
        self.assertEqual(testPostObj.post_content, "Updated Content")