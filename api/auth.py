from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class StudentManager(BaseUserManager):

  def create_user(self, username, email, password=None):
    if not username:
      raise ValueError("You must have a username")
    if not email:
      raise ValueError("You must have an email")

    user = self.model(
      username=username,
      email=self.normalize_email(email),
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, username, email, password):

    superuser = self.create_user(
      username=username,
      email=self.normalize_email(email),
      password=password,
    )

    superuser.is_admin = True
    superuser.is_staff = True
    superuser.is_superuser = True
    superuser.save(using=self._db)

    return superuser


class Student(AbstractBaseUser):
  username = models.CharField(max_length=20, unique=True)
  email = models.EmailField(max_length=50, unique=True)
  date_joined = models.DateTimeField(verbose_name='date joined', auto_now=True)
  last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  USERNAME_FIELD = 'username'
  EMAIL_FIELD = 'email'

  objects = StudentManager()

  REQUIRED_FIELDS = [
    'email',
  ]

  def __str__(self):
    return self.username

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self, app_label):
    return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


