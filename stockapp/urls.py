from . import views
from django.urls import path


urlpatterns = [
  path(route='', view=views.index, name='index'),
]