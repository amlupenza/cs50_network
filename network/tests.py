

from django.test import TestCase, Client
from .models import *
from django.contrib.auth import get_user_model
from datetime import datetime

# Create your tests here.
# test userModel
class UserModelTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password = 'testpass')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass'))
        self.assertEqual(User.objects.count(), 1)

# test PostModel
class PostModelTest(TestCase):
    # create a post
    def setUp(self):
        User = get_user_model()
        self.time = datetime.now()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(tweet='Hello, world!', author = self.user, time=self.time)

    def test_post(self):
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.tweet, 'Hello, world!')
        self.assertEqual(self.post.time, self.time)
        self.assertEqual(Post.objects.all().count(), 1)

# Client testing
    def test_index(self):
        # set up client to make request
        client = Client()
        response = client.get('')
        # ensure status code is 200
        self.assertEqual(response.status_code,200)
    def test_valid_profile(self):
        user = get_user_model()
        c = Client()
        response = c.get(f'/{user.id}')
        self.assertEqual(response.status_code,200)
        
