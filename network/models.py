from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# models for followers
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=True, blank=True)
    is_following = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} follows {self.target}: {self.is_following}"
# post model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweet')
    tweet = models.TextField(verbose_name='post', null=False, blank=False)
    liked_by = models.ManyToManyField(User, related_name='liked_posts')
    likes = models.IntegerField(null=True, blank=True, verbose_name='like', max_length=20, default=0)
    time = models.DateTimeField(verbose_name='creation time')

    def __str__(self):
        return self.tweet

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='comment', max_length=160)
    tweet = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',verbose_name='tweet')
    time = models.DateTimeField(verbose_name='creation date')
    liked_by = models.ManyToManyField(User, related_name='liked_comments')
    like = models.IntegerField(verbose_name='like',null=True, blank=True, max_length=20, default=0)

    def __str__(self) -> str:
        return self.comment


