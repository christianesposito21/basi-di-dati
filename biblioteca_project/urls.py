from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from gestione import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('registrazione/', views.register_view, name='registrazione'),
]
