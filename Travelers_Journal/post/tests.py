from django.test import TestCase
from django.contrib.auth.models import User
from post.models import Posts, React
from datetime import datetime
from django.db.models import Avg


# Create your tests here.

class OrmTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'travelersjournal',
            'password': 'aurora'}

        self.credentials2 = {
            'username': 'user2',
            'password': 'aurora'}

        self.credentials3 = {
            'username': 'user3',
            'password': 'aurora'}

        U1 = User.objects.create_user(**self.credentials)
        U2 = User.objects.create_user(**self.credentials2)
        U3 = User.objects.create_user(**self.credentials3)

        P1 = Posts.objects.create(post_title="Test Title", post_content="Test Content", post_date=datetime.now(), username=U1)
        P2 = Posts.objects.create(post_title="Test Title1", post_content="Test Content1",post_date=datetime.now(), username=U1)
        P3 = Posts.objects.create(post_title="Test Title2", post_content="Test Content2", post_date=datetime.now(), username=U1)

        React.objects.create(id=101, post_id=P1, username=U2, rating=4, comment='Comment By U2 on P1')
        React.objects.create(id=102, post_id=P1, username=U3, rating=5, comment='Comment By U3 on P1')

        React.objects.create(id=103, post_id=P2, username=U2, rating=1, comment='Comment By U2 on P2')
        React.objects.create(id=104, post_id=P2, username=U3, rating=5, comment='Comment By U3 on P2')
        React.objects.create(id=105, post_id=P2, username=U1, rating=1, comment='Comment By U1 on P2')

    '''
    Basisc ORM test of post class
    '''    
    def testORM(self):
        testPostObj = Posts.objects.get(post_title="Test Title")
        testPostObj1 = Posts.objects.get(post_title="Test Title1")
        self.assertEqual(testPostObj.post_content, "Test Content")
        self.assertEqual(testPostObj.post_title, "Test Title")
        self.assertIsNot(testPostObj.id, testPostObj1.id)
        self.assertIsNotNone(testPostObj)
    '''
    ORM test to check update
    '''
    def test_update(self):
        testPostObj = Posts.objects.get(post_title="Test Title")
        testPostObj.post_title = "Updated Title"
        testPostObj.post_content = "Updated Content"
        testPostObj.save()
        self.assertEqual(testPostObj.post_title, "Updated Title")
        self.assertEqual(testPostObj.post_content, "Updated Content")
    
    '''
    Test to check weather the username stored in the data base is same as the username who created the post
    '''
    def test_user(self):
        user = User.objects.get(username__in=['travelersjournal'])
        testPostObj2 = Posts.objects.get(post_title="Test Title2")
        self.assertEqual(testPostObj2.username, user)

    '''
    Basic ORM test of React Class/Table
    '''
    def test_react_basics(self):
        testReactObj = React.objects.get(id=101)
        testUserObj = User.objects.get(username__in=['user2'])
        self.assertEqual(testReactObj.rating, 4)
        self.assertEqual(testReactObj.comment, 'Comment By U2 on P1')
        self.assertEqual(testReactObj.username, testUserObj)
        self.assertIsInstance(testReactObj, React)
        self.assertNotIsInstance(testReactObj, User)

    '''
    Test to check the ratings of he posts.
    Gets average ratings and checks it
    Checks if no rating is given to a post, its average is None data type and vice versa
    '''
    def test_react_rating(self):
        testPostObj = Posts.objects.get(post_title="Test Title")
        testPostObj2 = Posts.objects.get(post_title="Test Title1")
        testPostObj3 = Posts.objects.get(post_title="Test Title2")

        ratingObj = React.objects.filter(post_id=testPostObj).aggregate((Avg('rating')))
        ratingObj2 = React.objects.filter(post_id=testPostObj2).aggregate((Avg('rating')))
        ratingObj3 = React.objects.filter(post_id=testPostObj3).aggregate((Avg('rating')))

        rating = round(ratingObj['rating__avg'], 2)
        rating2 = round(ratingObj2['rating__avg'], 2)

        self.assertEqual(rating, 4.5 )
        self.assertEqual(rating2, 2.33 )
        self.assertIsNone(ratingObj3['rating__avg'])
        self.assertIsNotNone(ratingObj2['rating__avg'])
    
    
    '''
    Checks the number of rating in a post.
    '''
    def test_react_cont(self):
        testPostObj = Posts.objects.get(post_title="Test Title")
        testPostObj2 = Posts.objects.get(post_title="Test Title1")
        testPostObj3 = Posts.objects.get(post_title="Test Title2")

        ratingObj = React.objects.filter(post_id=testPostObj).count()
        ratingObj2 = React.objects.filter(post_id=testPostObj2).count()
        ratingObj3 = React.objects.filter(post_id=testPostObj3).count()
        
        self.assertEqual(ratingObj, 2)
        self.assertEqual(ratingObj2, 3)
        self.assertEqual(ratingObj3, 0)
        self.assertIsNotNone(ratingObj3)
