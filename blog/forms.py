from django import forms
from django.contrib.auth.models import User

from .models import Blog, Profile

"""Das ist ein Test für die Dokumentation. Wir befinden uns hier grade in der Forms.py"""
class BlogForm(forms.ModelForm):
    """
    Form-Klasse zum Erstellen eines Blogs
    """
    class Meta:
        """
        Metadaten zum Erstellen der HTML-Form
        """
        model = Blog
        fields = ['title','content']
        labels = {
            'title': 'Titel',
            'content': 'Inhalt',
        }



class UpdateUserForm(forms.ModelForm):
    """
    Form-Klasse zum Bearbeiten eines Users
    """
    username = forms.CharField(max_length=30,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        """
        Metadaten zum Erstellen der HTML-Form
        """
        model = User
        fields = ['username']


class UpdateProfileForm(forms.ModelForm):
    """
    Form-Klasse zum Bearbeiten eines User-Profils, wird zusammen mit UpdateUserForm genutzt
    """
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        """
        Metadaten zum Erstellen der HTML-Form
        """
        model = Profile
        fields = ['avatar']
