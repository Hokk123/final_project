from django.urls import path
from .views import *
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('forklift/', ForkliftsList.as_view(), name = 'forklift_list'),
    path('forklift/<int:pk>/', ForkliftDetail.as_view(), name = 'forklift_detail'),
    path('forklift/create/', ForkliftCreate.as_view(), name = 'forklift_create'),
    path('forklift/<int:pk>/update/', ForkliftUpdate.as_view(), name = 'forklift_update'),
    path('forklift/<int:pk>/delete/', ForkliftDelete.as_view(), name = 'forklift_delete'),
    path('forklift/model_equipment/<int:pk>/',  ModelEquipmentDetail.as_view(), name = 'model_equipment_detail'),
    path('forklift/model_equipment/create/', ModelEquipmentCreate.as_view(), name = 'model_equipment_create'),
    path('forklift/model_equipment/<int:pk>/update/', ModelEquipmentUpdate.as_view(), name = 'model_equipment_update'),
    path('forklift/model_equipment/<int:pk>/delete/', ModelEquipmentDelete.as_view(), name = 'model_equipment_delete'),
    path('forklift/model_equipment/<int:pk>/', ModelEquipmentDetail.as_view(), name = 'model_equipment_detail'),
    path('forklift/engine_model/<int:pk>/', EngineModelDetail.as_view(), name = 'engine_model_detail'),
    path('forklift/engine_model/create/', EngineModelCreate.as_view(), name = 'engine_model_create'),
    path('forklift/engine_model/<int:pk>/update/', EngineModelUpdate.as_view(), name = 'engine_model_update'),
    path('forklift/engine_model/<int:pk>/delete/', EngineModelDelete.as_view(), name = 'engine_model_delete'),
    path('forklift/transmission_model/<int:pk>/', TransmissionModelDetail.as_view(), name = 'transmission_model_detail'),
    path('forklift/drive_axle_model/<int:pk>/', DriveAxleModelDetail.as_view(), name = 'drive_axle_model_detail'),
    path('forklift/controlled_bridge_model/<int:pk>/', ControlledBridgeModelDetail.as_view(), name = 'controlled_bridge_model_detail'),
    path('forklift/client_detail/<int:pk>/', ClientDetail.as_view(), name = 'client_detail'),
    path('forklift/service_company_detail/<int:pk>/', ServiceCompanyDetail.as_view(), name = 'service_company_detail'),
]