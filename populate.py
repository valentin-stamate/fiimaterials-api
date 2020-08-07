import os
os.environ.setdefault(
  'DJANGO_SETTINGS_MODULE',
  'server.settings'
)
import django
django.setup()

from api.auth import Student
from api.serializers import LinkSerializer, ClassSerializer, ResourceSerializer
from db_data import links, classes, resources
from api.models import Class, Resource


def populate():

  Class.objects.all().delete()

  for link in links:
    link_serializer = LinkSerializer(data=link)
    if link_serializer.is_valid():
      ins = link_serializer.save()
      print(ins.__str__() + " created or updated")

  for class_ in classes:
    class_serializer = ClassSerializer(data=class_)
    if class_serializer.is_valid():
      ins = class_serializer.save()
      print(ins.__str__() + " created or updated")

  for res in resources:
    resource = Resource.objects.get(id=res['id'])

    if resource is None:
      resource_serializer = ResourceSerializer(data=res)
      if resource_serializer.is_valid():
        ins = resource_serializer.save()
        print(ins.__str__() + " created")

    else:
      resource.title = res['title']
      resource.description = res['description']
      resource.image_url = res['image_url']
      resource.link_url = res['link_url']
      resource.tag_list = res['tag_list']

      print(resource.__str__() + " updated")

    resource.save()

  return 0


if __name__ == '__main__':
  print("Populating database...")
  populate()

