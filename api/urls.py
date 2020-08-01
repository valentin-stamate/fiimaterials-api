from django.urls import path

from api.views import get_classes, get_links

urlpatterns = [
  path('get/classes/', get_classes),
  path('get/links/', get_links)
]