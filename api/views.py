from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import ClassRating, Class, Link, Resource
from .serializers import ClassSerializer, LinkSerializer, SignupStudentSerializer, LoginStudentSerializer, \
  ResourceSerializer


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
    data.append(LinkSerializer(link).data)

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
    return Response(status=status.HTTP_400_BAD_REQUEST)

  student = login_serializer.save()

  token = Token.objects.get(user=student).key

  return Response(data={'token': token}, status=status.HTTP_200_OK)


class GetUser(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):

    data = {
      'username': request.user.username,
      'email': request.user.email,
    }

    return Response(data=data, status=status.HTTP_200_OK)


class SetRating(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):

    user = request.user
    new_rating = request.data['rating']

    if new_rating > 5 or new_rating < 1:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    class_instance = Class.objects.get(id=request.data['class_id'])
    class_rating, created = ClassRating.objects.get_or_create(
      student=user,
      class_name=class_instance,
    )

    class_rating.rating = new_rating
    class_rating.save()

    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def get_resources(request):

  res_list = []

  for res in Resource.objects.all():
    res_list.append(ResourceSerializer(res).data)

  return Response(data=res_list, status=status.HTTP_200_OK)


