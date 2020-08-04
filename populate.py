import os
os.environ.setdefault(
  'DJANGO_SETTINGS_MODULE',
  'server.settings'
)
import django
django.setup()

from api.auth import Student
from api.serializers import LinkSerializer, ClassSerializer
from db_data import links, classes
from api.models import Class


def populate():

  Class.objects.all().delete()

  for link in links:
    link_serializer = LinkSerializer(data=link)
    if link_serializer.is_valid():
      link_serializer.save()

  for class_ in classes:
    class_serializer = ClassSerializer(data=class_)
    if class_serializer.is_valid():
      class_serializer.save()

  return 0


if __name__ == '__main__':
  print("Populating database...")
  populate()

