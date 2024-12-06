from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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

    def get_object(self, queryset=None):
        # Hole das Blog-Objekt
        blog = super().get_object(queryset)
        # Erhöhe die Klickanzahl
        blog.clicks += 1
        blog.save()
        return blog

class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog_list')

class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog_list')
    template_name = 'blog/blog_delete.html'

class BlogDashboardView(ListView):
    model = Blog
    template_name = 'blog/blog_dashboard.html'  # Verwendet das neue Template
    context_object_name = 'latest_blogs'  # Kontextname für das QuerySet im Template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Neueste 5 Blogs
        context['latest_blogs'] = Blog.objects.all().order_by('-created_date')[:5]
        # 5 Blogs mit den meisten Klicks
        context['most_clicked_blogs'] = Blog.objects.all().order_by('-clicks')[:5]
        return context
