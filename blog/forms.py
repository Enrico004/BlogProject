from django import forms
from django.contrib.auth.models import User

from .models import Blog, Profile


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar']
