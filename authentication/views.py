from datetime import datetime

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from authentication.models import User

import re


# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        password = request.POST['password']

        # get timestamp
        timestamp = datetime.now().timestamp()

        user = User.objects.create_user(
            first_name=f_name,
            last_name=l_name,
            username=f_name + str(timestamp),
            email=email,
            password=password
        )
        user.save()

        login(request, user)
        return redirect('index')
    return render(request, 'authentication/signup.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'authentication/signin.html', {'error': 'User not found'})

        if not user.check_password(password):
            return render(request, 'authentication/signin.html', {'error': 'Incorrect password'})

        login(request, user)
        return redirect('index')

    return render(request, 'authentication/signin.html')


@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')


def validate_email(request):
    email = request.POST.get('email', '')
    action = request.POST.get('action', 'signup')

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(email_regex, email):
        return HttpResponse('Invalid email address')
    if User.objects.filter(email=email).exists() and action == 'signup':
        return HttpResponse('Email already exists')
    if not User.objects.filter(email=email).exists() and action == 'forgot-password':
        return HttpResponse('Email does not exist')

    return HttpResponse('')


def validate_password(request):
    password = request.POST['password']
    if len(password) < 8:
        return HttpResponse('Password must be at least 8 characters long')
    return HttpResponse('')


def validate_fname(request):
    f_name = request.POST['f_name'].strip().replace(" ", "")
    if not f_name.isalpha():
        return HttpResponse('First name must contain only alphabets')
    return HttpResponse('')


def validate_lname(request):
    l_name = request.POST['l_name'].strip().replace(" ", "")
    if not l_name.isalpha():
        return HttpResponse('Last name must contain only alphabets')
    return HttpResponse('')


def forgot_password(request):
    email = request.POST['email']
    if request.method == 'POST':
        user = User.objects.filter(email=email).first()
        user.send_password_reset_email(request)
    return HttpResponse('Email Sent')


def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(user)

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('sign-in')  # Redirect to a success page
        else:
            form = SetPasswordForm(user)
        return render(request, 'authentication/password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse('Password reset link is invalid or has expired.')
