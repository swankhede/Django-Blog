from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model):
    pic = models.ImageField(upload_to='media',blank=True, default='no-user.jpg')
    username = models.CharField(max_length=256)
    def __str__(self):
        return self.username 


class blogpost(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=1000)
    author = models.CharField(max_length=256)
    pic = models.ImageField(upload_to='media',blank=True)
    time =models.DateTimeField(auto_now=True, auto_now_add=False)
    
    
    def __str__(self):
        return self.title