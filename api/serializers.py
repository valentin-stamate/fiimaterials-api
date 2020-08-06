from rest_framework import serializers

from api.models import Link, Class, Student
import re


class LinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Link
    fields = ['name', 'link', 'type']


class ClassSerializer(serializers.ModelSerializer):
  class Meta:
    model = Class
    fields = ['id', 'name', 'name_short', 'average_rating', 'credits', 'year', 'semester',
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


class LoginStudentSerializer(serializers.Serializer):
  username_email = serializers.CharField(max_length=50)
  password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

  EMAIL_REGEX = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

  def create(self, validated_data):
    identifier = validated_data['username_email']  # username or password
    password = validated_data['password']
    student = None

    email_pattern = re.compile(self.EMAIL_REGEX)
    if email_pattern.match(identifier):
      student = Student.objects.get(email=identifier)
    else:
      student = Student.objects.get(username=identifier)

    if student is None:
      raise serializers.ValidationError("User don't exist")

    if not student.check_password(password):
      raise serializers.ValidationError("The password is wrong")

    return student

  def update(self, instance, validated_data):
    pass







