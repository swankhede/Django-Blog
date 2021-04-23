"""DBlog2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blogApp2 import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('post_blog/', views.post_blog, name='post_blog'),
    path('home/', views.home, name='home'),
    path('home/view_blog/<title>/<author>', views.view_blog, name='view_blog'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/delete/<pk>/', views.delete_blog, name='delete'),

    path('profile/edit/<pk>/', views.edit_blog, name='edit'),
    path('accounts/', views.edit_accounts, name='accounts'),
    path('user_accounts/<author>/', views.accounts, name='user_accounts')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
