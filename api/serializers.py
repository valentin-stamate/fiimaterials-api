from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import serializers

from api.models import Link, Class, Student, Resource, Feedback, ClassRating
import re
import string
import random


def random_token(length):
  letters = string.ascii_lowercase
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str


def sendemail(subject, template, context, email_to):

  html_message = render_to_string(template, context)
  plain_message = strip_tags(html_message)

  email_from = 'stamatevalentin64@gmail.com'

  send_mail(subject=subject, message=plain_message, from_email=email_from,
            recipient_list=email_to, html_message=html_message, fail_silently=False)


class LinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Link
    fields = ['name', 'link']


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

    verification_token = random_token(16)

    from api.models import VerificationToken
    VerificationToken(student=student, token=verification_token).save()

    email_context = {
      'token': verification_token,
      'username': student.username,
    }

    sendemail('Account Verification FIIMaterials', 'email_verification.html', email_context, [student.email])

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

    if not student.is_active:
      raise serializers.ValidationError("Account is not activated")

    return student

  def update(self, instance, validated_data):
    pass


class ResourceSerializer(serializers.ModelSerializer):

  class Meta:
    model = Resource
    fields = ['id', 'title', 'description', 'image_url', 'link_url', 'tag_list']


class FeedbackSerializer(serializers.ModelSerializer):

  class Meta:
    model = Feedback
    fields = ['id', 'student', 'name', 'show_name', 'implemented', 'feedback', 'date_created']


class ClassRatingSerializer(serializers.ModelSerializer):

  class Meta:
    model = ClassRating
    fields = ['student', 'class_name', 'rating']
