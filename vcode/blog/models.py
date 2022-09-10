import imp
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from xml.etree.ElementTree import Comment
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=20)
    slug = models.CharField(max_length=130)
    views = models.IntegerField(default=0)
    Timestamp=models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + ' by ' + self.author

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    # models.ForeignKey(User, on_delete=models.CASCADE) 
    # means jo mera user hai i.e Blogcomment will point at any record in the User 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    # means ya post jisko point kar raha hai agar usko delete kar 
    # diya jaata hai tho ya comment ka kya kar tho usko bhi delete kar dho 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True) 
    # self means it point to one of variable in BlogComment it also mean it will a comment reply or 
    # it may not be a reply of anytime it is comment itself 
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] +"..."+ "by" + self.user.username
