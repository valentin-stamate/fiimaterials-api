from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.auth import Student
from .models import StudentRating, Class, Link
from .serializers import ClassSerializer, LinkSerializer


@api_view(http_method_names=['GET'])
def get_classes(request):

  classes = Class.objects.all().filter(year=1)

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
    link_serializer = LinkSerializer(Link)
    data.append(link_serializer.data)

  return Response(data=data, status=status.HTTP_200_OK)


class UserData(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    return Response("done")

