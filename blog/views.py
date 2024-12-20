from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        likes_connected = get_object_or_404(Blog, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data

def blog_post_like(request, pk):
    post = get_object_or_404(Blog, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog_detail', args=[str(pk)]))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Übergibt einen leeren Blog-Objekt für den Zugriff auf Klicks/Likes
        context['blog'] = self.object or Blog(clicks=0, likes=0)
        return context

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