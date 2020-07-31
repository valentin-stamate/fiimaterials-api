from django.urls import path

from api.views import get_materials, get_useful_links

urlpatterns = [
  path('get-materials/', get_materials),
  path('get-useful-links', get_useful_links)
]

