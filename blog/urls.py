from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

urlpatterns= [
    path('list/', views.BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('create/', login_required(views.BlogCreateView.as_view()), name='blog_create'),
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('dashboard/', views.BlogDashboardView.as_view(), name='blog_dashboard'),


]