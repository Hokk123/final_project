from django.urls import path
from .views import *
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('forklift/', ForkliftsList.as_view(), name = 'forklift_list'),
    path('forklift/<int:pk>/', ForkliftDetail.as_view(), name = 'forklift_detail'),
    path('forklift/model_equipment/<int:pk>/',  ModelEquipmentDetail.as_view(), name = 'model_equipment_detail'),
    path('forklift/engine_model/<int:pk>/', EngineModelDetail.as_view(), name = 'engine_model_detail'),
    path('forklift/transmission_model/<int:pk>/', TransmissionModelDetail.as_view(), name = 'transmission_model_detail'),
    path('forklift/drive_axle_model/<int:pk>/', DriveAxleModelDetail.as_view(), name = 'drive_axle_model_detail'),
    path('forklift/controlled_bridge_model/<int:pk>/', ControlledBridgeModelDetail.as_view(), name = 'controlled_bridge_model_detail'),
    path('forklift/client_detail/<int:pk>/', ClientDetail.as_view(), name = 'client_detail'),
    path('forklift/service_company_detail/<int:pk>/', ServiceCompanyDetail.as_view(), name = 'service_company_detail'),
]