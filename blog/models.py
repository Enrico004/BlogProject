from django.contrib.auth.models import User
from django.db import models
from PIL import Image

# Create your models here.
class Blog(models.Model):
    """
    Modell der Beiträge
    enthält einen Titel, Inhalt, Aufrufe, Likes, Erstellungsdatum, Autor
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    clicks = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def number_of_likes(self):
        """
        Summiert die Anzahl der Likes, die der Beitrag hat
        :return: Summe der Likes
        """
        return self.likes.count()


class Profile(models.Model):
    """

    """
    avatar = models.ImageField(default='default.png',upload_to="profile_images")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """
        Überschreibt die Standard-Methode zum Speichern des Modells.
        Wenn das Bild die Standardgröße von 100x100 Pixel überschreitet, wird die Größe des Bilds angepasst
        :param args:
        :param kwargs:
        :return:
        """
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_size = (100, 100)
            img.thumbnail(new_size)
            img.save(self.avatar.path)
