from django.urls import path

from api.views import get_classes, get_links, signup_user, login_user

urlpatterns = [
  path('get/classes/', get_classes),
  path('get/links/', get_links),
  path('signup/', signup_user),
  path('login/', login_user),
]