"""Email URL Configuration

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
from apps.Main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login", views.login),
    path('signup', views.signup),
    path("new_account", views.signin_post),
    path("user_login", views.login_post),
    path("", views.home),
    path("new_message", views.new_message),
    path("send", views.send),
    path('show_messages', views.show_messages),
    path("message/<str:m_id>", views.message),
    path("sent", views.sent),
    path("get_sent", views.get_sent),
    path("logout", views.logout)
]
