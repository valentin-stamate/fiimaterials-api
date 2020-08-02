from rest_framework import serializers

from api.models import Link, Class


class LinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Link
    fields = ['name', 'link', 'type']


class ClassSerializer(serializers.ModelSerializer):
  class Meta:
    model = Class
    fields = ['name', 'name_short', 'average_rating', 'credits', 'year', 'semester',
              'material_link', 'site_link', 'site_password', 'votes_number']



