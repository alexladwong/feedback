"""
URL configuration for feedback_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

from feedback import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.feedback_list, name='feedback_list'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    
    path('profile/', views.profile, name='profile'),
    path('manage_subscription/<int:subscription_id>/', views.manage_subscription, name='manage_subscription'),
    path('user_feedback_history/', views.user_feedback_history, name='user_feedback_history'),
    path('feedback_analytics/', views.feedback_analytics, name='feedback_analytics'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit_feedback/<int:feedback_id>/', views.edit_feedback, name='edit_feedback'),
    path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    

]






