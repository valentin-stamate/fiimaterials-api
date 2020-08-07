from django.db import models

from .auth import Student


class Class(models.Model):
  id = models.IntegerField(primary_key=True, unique=True)

  name = models.CharField(max_length=50)
  name_short = models.CharField(max_length=10)
  average_rating = models.FloatField(default=0)
  credits = models.IntegerField()
  material_link = models.CharField(max_length=100, blank=True)
  site_link = models.CharField(max_length=100, blank=True)
  site_password = models.CharField(max_length=20, blank=True)

  year = models.IntegerField()
  semester = models.IntegerField()

  votes_number = models.IntegerField(default=0)
  updated_at = models.DateField(auto_now=True)

  def __str__(self):
    return self.name


class Link(models.Model):

  LINK_TYPES = (
    (1, "College Admission"),
    (2, "College Links"),
  )

  name = models.CharField(max_length=50, unique=True)
  link = models.CharField(max_length=50, unique=True)
  type = models.IntegerField(choices=LINK_TYPES)

  def __str__(self):
    return self.name


class ClassRating(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)

  class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
  rating = models.IntegerField(default=0)

  # def __str__(self):
  #   return ''


class Resource(models.Model):
  id = models.IntegerField(primary_key=True)

  title = models.CharField(max_length=50)
  description = models.CharField(max_length=255)
  image_url = models.CharField(max_length=200)
  link_url = models.CharField(max_length=200)
  tag_list = models.CharField(max_length=100)

  def __str__(self):
    return self.title



