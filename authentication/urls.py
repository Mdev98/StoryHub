from django.urls import path

from . import views

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign-up'),
    path('', views.sign_in, name='sign-in'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('validate-fname/', views.validate_fname, name='validate-fname'),
    path('validate-lname/', views.validate_lname, name='validate-lname'),
    path('validate-email/', views.validate_email, name='validate-email'),
    path('validate-password/', views.validate_password, name='validate-password'),

]