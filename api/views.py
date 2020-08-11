from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import ClassRating, Class, Link, Resource, Feedback
from .serializers import ClassSerializer, LinkSerializer, SignupStudentSerializer, LoginStudentSerializer, \
  ResourceSerializer, FeedbackSerializer
from django.utils import timezone


@api_view(http_method_names=['POST'])
def get_classes(request):

  year = request.data["year"]
  classes = Class.objects.all().filter(year=year).order_by('id')

  data = []
  for cls in classes:
    class_serializer = ClassSerializer(cls)
    data.append(class_serializer.data)

  return Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def get_links(request):

  links = Link.objects.all().order_by('id')

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
    rating_number = int(request.data['rating'])

    if rating_number > 5 or rating_number < 1:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    class_instance = Class.objects.get(id=request.data['class_id'])

    #
    class_rating, created = ClassRating.objects.get_or_create(
      student=user,
      class_name=class_instance,
    )

    votes_number = class_instance.votes_number
    class_rating_number = class_instance.average_rating

    if created:
      total_raw_rating = votes_number * class_rating_number + rating_number
      votes_number = votes_number + 1
      class_rating_number = total_raw_rating / votes_number
    else:
      old_rating = class_rating.rating
      total_raw_rating = votes_number * class_rating_number - old_rating + rating_number
      class_rating_number = total_raw_rating / votes_number

    class_instance.votes_number = votes_number
    class_instance.average_rating = class_rating_number
    class_instance.save()

    class_rating.rating = rating_number
    class_rating.save()

    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def get_resources(request):

  res_list = []

  for res in Resource.objects.all().order_by('id'):
    res_list.append(ResourceSerializer(res).data)

  return Response(data=res_list, status=status.HTTP_200_OK)


def get_all_feedback():
  feedback_list = Feedback.objects.all().order_by('id').reverse()

  data = []
  for feedback in feedback_list:
    data.append({
      'name': feedback.name if feedback.show_name and len(feedback.name) > 5 else 'Anonymous',
      'date_created': feedback.date_created,
      'implemented': feedback.implemented,
      'feedback': feedback.feedback,
    })

  return data


class PostFeedback(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):

    feedback = Feedback.objects.create(
      student=request.user,
      name=request.data['name'],
      feedback=request.data['feedback'],
      show_name=request.data['show_name'],
      date_created=timezone.now(),
    )
    feedback.save()

    return Response(data=get_all_feedback(), status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def get_feedback(request):

  return Response(data=get_all_feedback(), status=status.HTTP_200_OK)