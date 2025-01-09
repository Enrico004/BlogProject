from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from blog.forms import BlogForm, UpdateUserForm, UpdateProfileForm
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data = add_likes_to_data_context(self.kwargs['pk'],self.request.user.id,data)
        return data

def blog_post_like(request, pk):
    post = get_object_or_404(Blog, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return JsonResponse({'like-count':post.likes.count()})

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
        # Übergibt ein leeres Blog-Objekt für den Zugriff auf Klicks/Likes
        context['blog'] = self.object or Blog(clicks=0)
        return context


@login_required
def blog_post_like(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if blog.likes.filter(id=request.user.id).exists():
        # User already liked the post, so remove the like
        blog.likes.remove(request.user)
        liked = False
    else:
        # User has not liked the post, so add the like
        blog.likes.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': blog.likes.count()})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog_list')
    template_name = 'blog/blog_delete.html'

    def get_object(self, queryset=None):
        # Increment clicks only if the user is visiting (not liking)
        blog = super().get_object(queryset)
        if not self.request.user.is_authenticated or self.request.method == "GET":
            blog.clicks += 1
            blog.save()
        return blog

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


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'blog/change_password.html'
    success_url = reverse_lazy('blog_dashboard')
    success_message = 'Your password has been updated.'


class UserBlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_user_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        user = self.request.user

        return Blog.objects.filter(author=user)

def add_likes_to_data_context(blog_id,user_id,context):
    likes_connected = get_object_or_404(Blog, id=blog_id)
    liked = False
    if likes_connected.likes.filter(id=user_id).exists():
        liked = True
    context['number_of_likes'] = likes_connected.number_of_likes()
    context['post_is_liked'] = liked
    return context


@login_required
def profile(request):
    """
    view that handles updating of the user profile, allows user to set a profile picture
    :param request: request received from the frontend
    :return: returns either a redirect to the users profile page(POST) or the rendered
    forms to update the user profile
    """
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect(to='users-profile')
        pass
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'blog/profile.html', {'user_form': user_form, 'profile_form': profile_form})