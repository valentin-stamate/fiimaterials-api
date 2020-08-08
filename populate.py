import os
os.environ.setdefault(
  'DJANGO_SETTINGS_MODULE',
  'server.settings'
)
import django
django.setup()

from db_data import links, classes, resources
from api.models import Class, Resource, Link


def populate():
  #

  for link_ in links:
    link_ins, created = Link.objects.get_or_create(id=link_["id"])

    link_ins.name = link_["name"] # value too long for type character varying(50)
    link_ins.link = link_["link"]

    link_ins.save() # error on deploy
    print(link_ins.__str__() + " : created" if created else " : updated")

  #
  for class_ in classes:
    class_ins, created = Class.objects.get_or_create(id=class_['id'])

    class_ins.name = class_['name']
    class_ins.name_short = class_['name_short']
    class_ins.credits = class_['credits']
    class_ins.material_link = class_['material_link']
    class_ins.site_link = class_['site_link']
    class_ins.site_password = class_['site_password']
    class_ins.year = class_['year']
    class_ins.semester = class_['semester']

    class_ins.save()
    print(class_ins.__str__() + " : created" if created else " : updated")

  #
  for res in resources:
    resource, created = Resource.objects.get_or_create(id=res['id'])

    resource.title = res['title']
    resource.description = res['description']
    resource.image_url = res['image_url']
    resource.link_url = res['link_url']
    resource.tag_list = res['tag_list']

    resource.save()
    print(resource.__str__() + " : created" if created else " : updated")


  return 0


if __name__ == '__main__':
  print("Populating database...")
  populate()

