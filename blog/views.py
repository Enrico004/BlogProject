from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


# Create your views here.
class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog/blog_detail.html'

class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog_list')

class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog_list')
    template_name = 'blog/blog_delete.html'
