from django.db import models

from .auth import Student


class Class(models.Model):
  id = models.AutoField(primary_key=True)

  name = models.CharField(max_length=50, unique=True)
  name_short = models.CharField(max_length=10)
  average_rating = models.FloatField(default=0)
  credits = models.IntegerField()
  material_link = models.CharField(max_length=50, blank=True)
  site_link = models.CharField(max_length=50, blank=True)
  site_password = models.CharField(max_length=20, blank=True)
  year = models.IntegerField()

  votes_number = models.IntegerField(default=0)
  updated_at = models.DateField(auto_now=True)


class Link(models.Model):

  LINK_TYPES = (
    (1, "College Admission"),
    (2, "College Links"),
  )

  name = models.CharField(max_length=50, unique=True)
  link = models.CharField(max_length=50, unique=True)
  type = models.IntegerField(choices=LINK_TYPES)


class StudentRating(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)

  class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
  rating = models.IntegerField()



