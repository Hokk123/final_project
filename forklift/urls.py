from django.urls import path
from .views import *
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('forklift/', ForkliftsList.as_view(), name = 'forklift_list'),
    path('forklifts/<int:pk>/', ForkliftDetail.as_view(), name = 'forklift_detail'),
    path('forklifts/model_equipment/<int:pk>/',  ModelEquipmentDetail.as_view(), name = 'model_equipmentl_detail'),

]