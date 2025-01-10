from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from blog.forms import BlogForm, UpdateUserForm, UpdateProfileForm
from blog.models import Blog

class BlogListView(ListView):
    """
    View-Klasse für die Liste aller Beiträge
    """
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        """
        Überschreibt die Standard-Methode.
        Sammelt alle Beiträge des Nutzers, fügt die Anzahl der Likes hinzu und ordnet sie nach dem Erstellungsdatum
        :return: Liste von Blog-Objekten
        """
        return Blog.objects.annotate(like_count=Count('likes')).order_by('created_date')

class BlogDetailView(DetailView):
    """
    View-Klasse zur Darstellung einer Detail-View
    """
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog/blog_detail.html'


    def get_object(self, queryset=None):
        """
        Überschreibt Standard-Methode. Inkrementiert die Anzahl an Aufrufen, sobald Detail-Seite aufgerufen wird
        :param queryset:
        :return: Beitrag mit inkrementiert Anzahl an aufrufen
        """
        # Hole das Blog-Objekt
        blog = super().get_object(queryset)
        # Erhöhe die Klickanzahl
        blog.clicks += 1
        blog.save()
        return blog

    def get_context_data(self, **kwargs):
        """
        Überschreibt Standard-Methode. Fügt die Anzahl der Likes zum Kontext hinzu
        :param kwargs:
        :return: Überarbeiteter Kontext
        """
        data = super().get_context_data(**kwargs)
        data = add_likes_to_data_context(self.kwargs['pk'],self.request.user.id,data)
        return data


class BlogCreateView(CreateView):
    """
    View-Klasse zum Erstellen eines Beitrags
    """
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blogs:blog_list')

    def form_valid(self, form):
        """
        Überschreiben der Standard-Methode. Fügt aktuellen Nutzer als Autor hinzu
        :param form: Aktuelle bearbeitete From
        :return: HttpResponseRedirect abhängig von der Validität
        """
        # Get authenticated user and set it as the blog author
        # authenticated user is guaranteed because of login_required in urls.py
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Bearbeitet den bereits erstellten Kontext. Setzt die Anzahl an Aufrufen auf 0
        :param kwargs:
        :return: Überarbeiter Kontext
        """
        context = super().get_context_data(**kwargs)
        # Übergibt ein leeres Blog-Objekt für den Zugriff auf Klicks/Likes
        context['blog'] = self.object or Blog(clicks=0)
        return context


@login_required
def blog_post_like(request, pk):
    """
    Funktion zum Liken/Unliken eines Beitrags. Wenn der User den Beitrag bereits geliked hat, wird dieser entfernt. Ansonsten wird ein Like hinzugefügt
    :param request: Anfrage vom Frontend
    :param pk: Primärschlüssel des Beitrags
    :return: JSON mit der Anzahl an Likes(like_count) und ob der User den Beitrag geliked hat(liked)
    """
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
    """
    Klasse zum Löschen von Beiträgen
    """
    model = Blog
    success_url = reverse_lazy('blogs:blog_list')
    template_name = 'blog/blog_delete.html'


class BlogDashboardView(ListView):
    """
    View-Klasse für die Dashboard-View
    """
    model = Blog
    template_name = 'blog/blog_dashboard.html'  # Verwendet das neue Template
    context_object_name = 'latest_blogs'  # Kontextname für das QuerySet im Template

    def get_queryset(self):
        """
        Überschreibt die Standard-Methode.
        Sammelt alle Beiträge, fügt die Anzahl der Likes hinzu und ordnet sie nach dem Erstellungsdatum
        :return: Liste von Blog-Objekten
        """
        return Blog.objects.annotate(like_count=Count('likes')).order_by('created_date')

    def get_context_data(self, **kwargs):
        """
        Überschreibt standard-Methode. Fügt dem Kontext die 5 letzten und 5 meistgeklickten Beiträge hinzu
        :param kwargs:
        :return: Kontext zur Verarbeitung im Frontend
        """
        context = super().get_context_data(**kwargs)
        # Neueste 5 Blogs
        context['latest_blogs'] = Blog.objects.all().annotate(like_count=Count('likes')).order_by('-created_date')[:5]
        # 5 Blogs mit den meisten Klicks
        context['most_clicked_blogs'] = Blog.objects.all().annotate(like_count=Count('likes')).order_by('-clicks')[:5]
        return context

class SignupView(CreateView):
    """
    View-Klasse zum Erstellen eines neuen Nutzers.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('blogs:login')
    template_name = 'registration/signup.html'


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """
    View-Klasse zum Ändern des Nutzerpassworts
    Bei Erfolg wird der Nutzer an das Dashboard weitergeleitet
    """
    template_name = 'blog/change_password.html'
    success_url = reverse_lazy('blogs:blog_dashboard')
    success_message = 'Your password has been updated.'


class UserBlogListView(ListView):
    """
    View-Klasse für nutzerspezifische Beiträge
    """
    model = Blog
    template_name = 'blog/blog_user_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        """
        Überschreibt die Standard-Methode.
        Sammelt alle Beiträge des Nutzers, fügt die Anzahl der Likes hinzu und ordnet sie nach dem Erstellungsdatum
        :return: Liste von Blog-Objekten
        """
        user = self.request.user

        return Blog.objects.filter(author=user).annotate(like_count=Count('likes')).order_by('-created_date')

def add_likes_to_data_context(blog_id,user_id,context):
    """
    Methode, mit welcher die Anzahl der Likes zum Kontext hinzugefügt werden
    :param blog_id: Id des Beitrags, für den die Likes hinzugefügt werden sollen
    :param user_id: Nutzer, der die Anfrage gestellt hat
    :param context: Bereits erstellter Kontext, der ans Frontend gegeben wird. Die Anzahl an Likes und ob der Post vom Nutzer bereits geliked wurde, wird dem Kontext hinzugefügt
    :return: Kontext mit Anzahl an Likes(number_of_likes) und boolean post_is_liked
    """
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
    View für das Updaten der User-Profile. Erlaubt das Ändern von Nutzernamen und Profilbilds
    :param request: Anfrage vom Frontend
    :return: Redirect zur Profil-Seite des Nutzers oder die Form zum Updaten des Profils (abhängig von der Anfrage-Methode)
    """
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'blog/profile.html', {'user_form': user_form, 'profile_form': profile_form})