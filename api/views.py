from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.auth import Student
from api.models import StudentRating


@api_view(http_method_names=['GET'])
def get_materials(request):
  print("dkas")
  return Response("done")


@api_view(http_method_names=['GET'])
def get_useful_links(request):
  return Response("dome")


class UserData(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    return Response("done")

