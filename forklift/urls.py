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
    path('forklift/transmission_model/create/', TransmissionModelCreate.as_view(), name = 'transmission_model_create'),
    path('forklift/transmission_model/<int:pk>/update/', TransmissionModelUpdate.as_view(), name = 'transmission_model_update'),
    path('forklift/transmission_model/<int:pk>/delete/', TransmissionModelDelete.as_view(), name = 'transmission_model_delete'),
    path('forklift/drive_axle_model/<int:pk>/', DriveAxleModelDetail.as_view(), name = 'drive_axle_model_detail'),
    path('forklift/drive_axle_model/create/', DriveAxleModelCreate.as_view(), name = 'drive_axle_model_create'),
    path('forklift/drive_axle_model/<int:pk>/update/', DriveAxleModelUpdate.as_view(), name = 'drive_axle_model_update'),
    path('forklift/drive_axle_model/<int:pk>/delete/', DriveAxleModelDelete.as_view(), name = 'drive_axle_model_delete'),
    path('forklift/controlled_bridge_model/<int:pk>/', ControlledBridgeModelDetail.as_view(), name = 'controlled_bridge_model_detail'),
    path('forklift/controlled_bridge_model/create/', ControlledBridgeModelCreate.as_view(), name = 'controlled_bridge_model_create'),
    path('forklift/controlled_bridge_model/<int:pk>/update/', ControlledBridgeModelUpdate.as_view(), name = 'controlled_bridge_model_update'),
    path('forklift/controlled_bridge_model/<int:pk>/delete/', ControlledBridgeModelDelete.as_view(), name = 'controlled_bridge_model_delete'),
    path('to/', ToList.as_view(), name = 'To_list'),
    path('to/<int:pk>/', ToDetail.as_view(), name = 'To_detail'),
    path('to/create/', ToCreate.as_view(), name = 'To_create'),
    path('to/<int:pk>/update/', ToUpdate.as_view(), name = 'To_update'),
    path('to/<int:pk>/delete/', ToDelete.as_view(), name = 'To_delete'),
    path('forklift/client_detail/<int:pk>/', ClientDetail.as_view(), name = 'client_detail'),
    path('forklift/service_company_detail/<int:pk>/', ServiceCompanyDetail.as_view(), name = 'service_company_detail'),
]