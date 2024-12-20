from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    clicks = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)