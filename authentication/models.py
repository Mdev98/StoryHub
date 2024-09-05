from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from blog.utils import send_email


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Create your models here.

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('subscriber', 'Subscriber'),
        ('creator', 'Creator'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='subscriber')

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.is_staff

    def is_subscriber(self):
        return self.role == 'subscriber'

    def is_creator(self):
        return self.role == 'creator'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def send_password_reset_email(self, request):
        """
        Sends a password reset email to the user.
        """
        token = default_token_generator.make_token(self)
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        current_site = get_current_site(request)
        domain = current_site.domain
        protocol = 'https' if request.is_secure() else 'http'

        reset_url = f"{protocol}://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
        subject = 'Password Reset Request'
        message = render_to_string('authentication/password_reset_email.html', {
            'user': self,
            'reset_url': reset_url,
            'domain': domain,
            'uid': uid,
            'token': token,
        })

        send_email('mamour.diop22@gmail.com', subject, message)


