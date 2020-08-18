from django.urls import path

from api.views import get_classes, get_links, signup_user, login_user, GetUserData, SetRating, get_resources, get_feedback, \
  PostFeedback, verify_email

urlpatterns = [
  path('get/classes/', get_classes),
  path('get/links/', get_links),
  path('signup/', signup_user),
  path('login/', login_user),
  path('get/user-data/', GetUserData.as_view()),
  path('post/rating/', SetRating.as_view()),
  path('get/resources/', get_resources),
  path('get/feedback/', get_feedback),
  path('post/feedback/', PostFeedback.as_view()),
  path('verify-email/', verify_email)
]