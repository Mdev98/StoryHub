from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('update-name/', views.update_name, name='update-name'),
    path('update-password/', views.update_password, name='update-password'),
]