from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    clicks = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def number_of_likes(self):
        return self.likes.count()

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
