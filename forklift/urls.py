from django.urls import path
from .views import *
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('cars/', CarsList.as_view(), name = 'car_list'),

]