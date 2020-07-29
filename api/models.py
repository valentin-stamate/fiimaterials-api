from django.db import models
from .auth import Student


class Class(models.Model):
  class_year = models.IntegerField()
  class_name = models.CharField(max_length=50)
  average_rating = models.FloatField(default=0)
  material_link = models.CharField(max_length=50)
  site_link = models.CharField(max_length=50)


class UsefulLink(models.Model):

  LINK_TYPES = (
    (1, "College Admission"),
    (2, "College Links"),
  )

  name = models.CharField(max_length=50)
  link = models.CharField(max_length=50)
  type = models.IntegerField(choices=LINK_TYPES)




