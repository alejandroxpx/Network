from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.id} {self.username} {self.password}"

# User who commented, User who was commented on, date of comment, like count, 
class Comment(models.Model):
    # id = models.AutoField()
    comment = models.CharField(max_length=64)
    user_commenting = models.ForeignKey(User, on_delete=models.CASCADE,related_name="commentor")
    user_being_commented = models.ForeignKey(User, on_delete=models.CASCADE,related_name="commentee")
    date = models.DateTimeField(auto_now_add = True)
    likes = models.IntegerField()

    def __str__(self):
        return f"{self.id} {self.user_being_commented} commenting on {self.user_being_commented}: {self.comment} {self.date} {self.likes}."

# User, post, date, comments, likes
class Post(models.Model):
    # id = models.AutoField()
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    post = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} {self.user}: {self.post} {self.date} {self. comments} {self.likes}."

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ForeignKey(User,related_name="followers",on_delete=models.CASCADE,default=0)
    following = models.ForeignKey(User,related_name="following",on_delete=models.CASCADE,default=0)
    post_created_by_user = models.ForeignKey(Post,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return f"{self.id} {self.user}"



