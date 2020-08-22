from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .auth import Student
from .models import ClassRating, Class, Link, Resource, Feedback, VerificationToken, About
from .serializers import ClassSerializer, LinkSerializer, SignupStudentSerializer, LoginStudentSerializer, \
  ResourceSerializer, AboutSerializer
from django.utils import timezone
from .utils import decrypt, sendemail, random_token, validate_email


@api_view(http_method_names=['GET'])
def get_about(request):

  data = []

  for about in About.objects.all().order_by('id'):
    data.append(AboutSerializer(about).data)

  return Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def recover_password(request):
  email = request.data['email']

  if not validate_email(email):
    return Response(status=status.HTTP_400_BAD_REQUEST)

  user = Student.objects.get(email=email) # if the user is not found, then it will trow an error
  username = user.username

  token = random_token(16)

  context = {
    'username': username,
    'token': token,
  }

  # I should DRY my hands here
  verification_token, created = VerificationToken.objects.get_or_create(student=user, type=3)
  verification_token.token = token
  verification_token.save()

  sendemail(subject='Recover Password', template='recover_password.html',context=context, email_to=[email])

  return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
  user = request.user

  new_username = request.data['username']
  new_email = request.data['email']
  new_password = request.data['new_password']
  current_password = request.data['password']

  if not user.check_password(current_password):
    return Response(data='Wrong password', status=status.HTTP_400_BAD_REQUEST)

  if len(new_username) < 8:
    return Response(data='Your new password should be at least 8 characters', status=status.HTTP_400_BAD_REQUEST)

  if new_email != '' and not validate_email(new_email):
    return Response(data='Invalid email', status=status.HTTP_400_BAD_REQUEST)

  if len(new_password) != 0 and len(new_password) < 8:
    return Response(data='Invalid password', status=status.HTTP_400_BAD_REQUEST)

  if user.username != new_username:
    user.username = new_username

  if new_email != '' and user.email != new_email:
    token = random_token(16)
    email_context = {
      'token': token,
      'username': user.username,
    }

    verification_token, created = VerificationToken.objects.get_or_create(student=user, type=2)
    verification_token.new_email = new_email
    verification_token.token = token
    verification_token.save()

    sendemail(subject='New Email', template='change_email.html', context=email_context,
              email_to=[new_email])

  if len(new_password) != 0:
    user.set_password(new_password)

  user.save()

  logout(request)

  return Response(data="Profile Updated", status=200)


@api_view(http_method_names=['POST'])
def verify_token(request):
  token = request.data['token']
  verification_token = VerificationToken.objects.get(token=token)
  user = verification_token.student

  message = ''
  if verification_token.type == 1:
    user.is_active = True
    message = 'Account activated'

  if verification_token.type == 2:
    new_email = verification_token.new_email
    user.email = new_email
    message = 'Email updated'

  if verification_token.type == 3:
    new_password = request.data['password']
    user.set_password(new_password)
    message = 'Password changed'

  user.save()
  verification_token.delete()

  return Response(data=message, status=status.HTTP_200_OK)


def get_all_classes(year, user):

  classes = Class.objects.all().filter(year=year).order_by('id')

  data = []
  for cls in classes:
    class_rating = None
    rating = 0.0

    if user.is_authenticated:
      class_rating = ClassRating.objects.all().filter(student=user, class_name=cls).first()

    if class_rating:
      rating = class_rating.rating

    class_serializer = ClassSerializer(cls).data
    class_serializer['user_rating'] = rating
    data.append(class_serializer)

  return data


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def get_classes(request):

  return Response(data=get_all_classes(request.data['year'], request.user), status=status.HTTP_200_OK)


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
    signup_serializer.save()
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)

  return Response(status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
def login_user(request):

  login_serializer = LoginStudentSerializer(data=request.data)

  if not login_serializer.is_valid():
    return Response(status=status.HTTP_400_BAD_REQUEST)

  student = login_serializer.save()

  token = Token.objects.get(user=student).key

  return Response(data={'token': token}, status=status.HTTP_200_OK)


class GetUserData(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):

    user = request.user

    favorite_courses = []
    for class_rating in ClassRating.objects.filter(student=user, rating=5):
      favorite_courses.append(class_rating.class_name.name)

    data = {
      'username': user.username,
      'email': user.email,
      'date_joined': user.date_joined.date(),
      'last_login': user.last_login.date(),
      'is_superuser': user.is_superuser,
      'favorite_courses': favorite_courses,
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

    year = class_instance.year

    return Response(data=get_all_classes(year, request.user), status=status.HTTP_200_OK)


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


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_rating(request):
  user = request.user
  class_id = request.data['class_id']

  class_ = Class.objects.get(id=class_id)
  class_year = class_.year
  class_rating = ClassRating.objects.get(student=user, class_name=class_)

  rating = class_rating.rating
  class_rating.delete()

  average_rating = class_.average_rating
  votes_number = class_.votes_number
  total_sum = average_rating * votes_number

  total_sum = total_sum - rating
  votes_number = votes_number - 1

  class_.votes_number = votes_number
  class_.average_rating = total_sum / votes_number if votes_number != 0 else 0

  class_.save()

  return Response(data=get_all_classes(class_year, user), status=status.HTTP_200_OK)


