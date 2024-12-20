from django.contrib.auth.forms import UserCreationForm
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

    def get_object(self, queryset=None):
        # Hole das Blog-Objekt
        blog = super().get_object(queryset)
        # Erhöhe die Klickanzahl
        user_is_author = blog.author == self.request.user
        if user_is_author:
            blog.clicks += 1
            blog.save()
        return blog

class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        # Get authenticated user and set it as the blog author
        # authenticated user is guaranteed because of login_required in urls.py
        form.instance.author = self.request.user
        return super().form_valid(form)

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

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserBlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_user_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author=user)