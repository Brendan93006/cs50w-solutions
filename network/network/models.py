from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField()

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like")

class comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")

