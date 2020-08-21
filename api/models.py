from django.db import models
from .auth import Student


class VerificationToken(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)

  CHOICES = [
    (1, 'Account Verification'),
    (2, 'New Email'),
    (3, 'Recover Password'),
  ]
  type = models.IntegerField(choices=CHOICES)

  new_email = models.EmailField(max_length=50, blank=True)

  token = models.CharField(max_length=20)

  def __str__(self):
    return self.token


class Class(models.Model):
  id = models.IntegerField(primary_key=True, unique=True)

  name = models.CharField(max_length=50)
  name_short = models.CharField(max_length=10)
  credits = models.IntegerField(blank=True, null=True)
  material_link = models.CharField(max_length=100, blank=True, null=True)
  site_link = models.CharField(max_length=100, blank=True, null=True)
  site_password = models.CharField(max_length=20, blank=True, null=True)

  year = models.IntegerField(blank=True, null=True)
  semester = models.IntegerField(blank=True, null=True)

  votes_number = models.IntegerField(default=0)
  average_rating = models.FloatField(default=0)
  updated_at = models.DateField(auto_now=True)

  def __str__(self):
    return self.name


class Link(models.Model):
  id = models.IntegerField(primary_key=True, unique=True)

  name = models.CharField(max_length=255)
  link = models.CharField(max_length=255)

  def __str__(self):
    return self.name


class ClassRating(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)

  class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
  rating = models.IntegerField(default=0)

  def __str__(self):
    return str(self.rating)


class Resource(models.Model):
  id = models.IntegerField(primary_key=True, unique=True)

  title = models.CharField(max_length=50)
  description = models.TextField(blank=True)
  image_url = models.CharField(max_length=200)
  link_url = models.CharField(max_length=200)
  tag_list = models.CharField(max_length=100)

  def __str__(self):
    return self.title


class Feedback(models.Model):
  id = models.AutoField(primary_key=True)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)

  name = models.CharField(max_length=30, blank=True)
  show_name = models.BooleanField(default=True)
  implemented = models.BooleanField(default=False)
  feedback = models.CharField(max_length=255)

  date_created = models.DateField(auto_created=True)

  def __str__(self):
    return self.name

