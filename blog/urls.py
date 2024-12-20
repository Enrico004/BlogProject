from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views
from .views import SignupView

urlpatterns= [
    path('list/', views.BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('create/', login_required(views.BlogCreateView.as_view()), name='blog_create'),
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('user/posts/',views.UserBlogListView.as_view(), name='user_blog_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("signup/", SignupView.as_view(), name="signup"),
    path('dashboard/', views.BlogDashboardView.as_view(), name='blog_dashboard'),
    path('blogpost-like/<int:pk>', views.blog_post_like, name="blogpost_like"),

]