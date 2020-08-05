from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from api.auth import Student
from .models import StudentRating, Class, Link
from .serializers import ClassSerializer, LinkSerializer, SignupStudentSerializer, LoginStudentSerializer


@api_view(http_method_names=['POST'])
def get_classes(request):

  year = request.data["year"]
  classes = Class.objects.all().filter(year=year)

  data = []
  for cls in classes:
    class_serializer = ClassSerializer(cls)
    data.append(class_serializer.data)

  return Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def get_links(request):

  links = Link.objects.all()

  data = []
  for link in links:
    link_serializer = LinkSerializer(link)
    data.append(link_serializer.data)

  return Response(data=data, status=status.HTTP_200_OK)


class UserData(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    return Response("done")


# TODO check for duplicate username, email
@api_view(http_method_names=['POST'])
def signup_user(request):

  signup_serializer = SignupStudentSerializer(data=request.data)
  if signup_serializer.is_valid():
    student = signup_serializer.save()
  else:
    return Response(status=status.HTTP_206_PARTIAL_CONTENT)

  token = Token.objects.get(user=student).key

  return Response(data={'token': token}, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
def login_user(request):

  login_serializer = LoginStudentSerializer(data=request.data)

  if not login_serializer.is_valid():
    return Response(status=status.HTTP_206_PARTIAL_CONTENT)

  student = login_serializer.save()

  token = Token.objects.get(user=student).key

  return Response(data={'token': token}, status=status.HTTP_200_OK)







