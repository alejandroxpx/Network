from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# User who commented, User who was commented on, date of comment, like count, 
class Comments(models.Model):
    comment = models.CharField(max_length=128)
    user_commenting = models.ForeignKey(User, on_delete=models.CASCADE,related_name="commentor")
    user_being_commented = models.ForeignKey(User, on_delete=models.CASCADE,related_name="commentee")
    date = models.DateTimeField(auto_now_add = True)
    likes = models.IntegerField()

# User, post, date, comments, likes
class NewPost(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    post = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comments, blank=True)
    likes = models.IntegerField()



