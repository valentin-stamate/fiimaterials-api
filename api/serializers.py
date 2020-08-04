from rest_framework import serializers

from api.models import Link, Class, Student


class LinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Link
    fields = ['name', 'link', 'type']


class ClassSerializer(serializers.ModelSerializer):
  class Meta:
    model = Class
    fields = ['name', 'name_short', 'average_rating', 'credits', 'year', 'semester',
              'material_link', 'site_link', 'site_password', 'votes_number']


class SignupStudentSerializer(serializers.ModelSerializer):
  re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

  class Meta:
    model = Student
    fields = ['username', 'email', 'password', 're_password']
    extra_kwargs = {
      'password': {'write_only': True},
    }

  def create(self, validated_data):

    password = validated_data['password']
    re_password = validated_data['re_password']

    if password != re_password:
      raise serializers.ValidationError({'password': 'The password must match'})

    student = Student(
      username=validated_data['username'],
      email=validated_data['email'],
    )
    student.set_password(password)
    student.save()

    return student

