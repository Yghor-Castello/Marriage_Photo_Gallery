from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager

from users.constants import USER_TYPE


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    name = models.CharField('Name', max_length=255)
    email = models.EmailField('E-mail', unique=True)
    user_type = models.CharField('User Type', max_length=25, choices=USER_TYPE)
    is_superuser = models.BooleanField('Super User', default=True)
    username = models.CharField('Username', max_length=100, unique=True, null=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def is_authorized_to_upload(self):
        return self.user_type in ['groom', 'bride']

    objects = UserManager()




