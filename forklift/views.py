from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import *

from .models import *
from .filters import ForkliftFilter, ToFilter, ClaimFilter


#Миксины
class ForkliftListMixin(object,):
    model = Forklift

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_superuser or user.groups.filter(name = 'manager').exists() or not user.is_authenticated:
            return
        else:
            return queryset.filter(Q(client__user = user) | Q(service_company__user = user))

class ToListMixin(object,):
    model = To

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_superuser or user.groups.filter(name = 'manager').exists():
            return 
        else:
            return queryset.filter(Q(car__client__user = user) | Q(service_company__user = user))
        
        
class ClaimListMixin(object,):
    model = Claim

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_superuser or user.groups.filter(name = 'manager').exists():
            return 
        else:
            return queryset.filter(Q(car__client__user = user) | Q(service_company__user = user))



#Погрузчики
class ForkliftsList(LoginRequiredMixin, ListView, ForkliftListMixin):
    #указываем модель, объекты которой мы будем выводить
    model = Forklift
    form_class = ForkliftForm
    # #поле, которое будет использоваться для сортировки объектов
    ordering = '-date_of_shipment'
    #указываем имя шаблона, в котором будут все инструкции о том
    #как именно пользователю должны быть показаны наши объекты
    template_name = 'forklift/forklifts.html'
    #это имя списка, в котором будут лежать все объекты.
    #его надо указать, чтобы обратиться к списку объекту в html-шаблоне.
    context_object_name = 'forklifts'


    # Переопределяем функцию получения списка машин
    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = ForkliftFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список машин
       return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       #проверяем принадлежность пользователя к группе для отображения кнопки создания машины
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       user_in_group_service_complany = self.request.user.groups.filter(name='service_company').exists()
       context['user_in_group_manager'] = user_in_group_manager
       context['user_in_group_service_company'] = user_in_group_service_complany
       return context


class ForkliftDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView, PermissionRequiredMixin):
    model = Forklift
    template_name = 'forklift/forklift.html'
    context_object_name = 'forklift'
    permission_required = ('forklift.view_forklift', )

    def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.client.user == datauser or obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context


class ForkliftCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = ForkliftForm
   model = Forklift
   template_name = 'forklift/forklift_edit.html'
   permission_required = 'forklift.add_forklift'

class ForkliftUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = ForkliftForm
   model = Forklift
   template_name = 'forklift/forklift_edit.html'
   permission_required = 'forklift.change_forklift'

class ForkliftDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   model = Forklift
   template_name = 'forklift/Forklift_delete.html'
   success_url = reverse_lazy('forklift_list')
   permission_required = 'forklift.delete_forklift'



#Модель погрузчика
class ModelEquipmentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = ModelEquipment
   template_name = 'forklift/model_equipment.html'
   context_object_name = 'model_equipment'

   def test_func(self):
      datauser = self.request.user
      if(datauser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         forklifts = Forklift.objects.all()
         for forklift in forklifts:
            technique_model = forklift.technique_model
            if(self.get_object() == technique_model and (forklift.client.user == datauser or forklift.service_company.user == datauser)):
               return True
         return False
         
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context

class ModelEquipmentCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = ModelEquipmentForm
   model = ModelEquipment
   template_name = 'forklift/model_equipment_edit.html'
   permission_required = 'forklift.add_modelequipment'

class ModelEquipmentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = ModelEquipmentForm
   model = ModelEquipment
   template_name = 'forklift/model_equipment_edit.html'
   permission_required = 'forklift.change_modelequipment'

class ModelEquipmentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   form_class = ModelEquipmentForm
   model = ModelEquipment
   template_name = 'forklift/model_equipment_delete.html'
   permission_required = 'forklift.delete_modelequipment'



#ТО
class ToList(LoginRequiredMixin, ListView, ToListMixin):
    model = To
    template_name = 'forklift/to_list.html'
    context_object_name = 'to'
    permission_required = 'forklift.view_to'

    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = ToFilter(self.request.GET, queryset)
       return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['filterset'] = self.filterset
       context['ordering'] = self.ordering
       return context

class ToDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = To
    template_name = 'forklift/to_list.html'
    context_object_name = 'to'
    permission_required = 'forklift.view_to'
    
    def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.car.client.user == datauser or obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()

class ToCreate(LoginRequiredMixin, CreateView):
   form_class = ToForm
   model = To
   template_name = 'forklift/to_edit.html'
   permission_required = 'forklift.add_to'

class ToUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
   form_class = ToForm
   model = To
   template_name = 'forklift/to_edit.html'
   permission_required = 'forklift.change_to'

   def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.car.client.user == datauser or obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()

class ToDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = To
   template_name = 'forklift/to_delete.html'
   success_url = reverse_lazy('to_list')
   permission_required = 'forklift.delete_to'

   def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.car.client.user == datauser or obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()


#Тип ТО
class TypeToDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = TypeTo
   template_name = 'forklift/type_to.html'
   context_object_name = 'type_to'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         tos = to.objects.all()
         for to in tos:
            type_to = to.type_to
            if(self.get_object() == type_to and (to.car.client.user == datauser or to.service_company.user == datauser)):
               return True
         return False
      
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context
      
class TypeToCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = TypeToForm
   model = TypeTo
   template_name = 'forklift/type_to_edit.html'
   permission_required = 'forklift.add_typeofto'

class TypeToUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = TypeToForm
   model = TypeTo
   template_name = 'forklift/type_to_edit.html'
   permission_required = 'forklift.change_typeofto'

class TypeToDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   form_class = TypeToForm
   model = TypeTo
   template_name = 'forklift/type_to_delete.html'
   permission_required = 'forklift.delete_typeofto'



#Двигатель
class EngineModelDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = EngineModel
   template_name = 'forklift/engine_model.html'
   context_object_name = 'engine_model'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         forklifts = Forklift.objects.all()
         for forklift in forklifts:
            engine_model = forklift.engine_model
            if(self.get_object() == engine_model and (forklift.client.user == datauser or forklift.service_company.user == datauser)):
               return True
         return False
      
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context
      
class EngineModelCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = EngineModelForm
   model = EngineModel
   template_name = 'forklift/engine_model_edit.html'
   permission_required = 'forklift.add_enginemodel'

class EngineModelUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = EngineModelForm
   model = EngineModel
   template_name = 'forklift/engine_model_edit.html'
   permission_required = 'forklift.change_enginemodel'

class EngineModelDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   form_class = EngineModelForm
   model = EngineModel
   template_name = 'forklift/engine_model_delete.html'
   permission_required = 'forklift.delete_enginemodel'



#Трансмиссия
class TransmissionModelDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = TransmissionModel
   template_name = 'forklift/transmission_model.html'
   context_object_name = 'transmission_model'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         forklifts = Forklift.objects.all()
         for forklift in forklifts:
            transmission_model = forklift.transmission_model
            if(self.get_object() == transmission_model and (forklift.client.user == datauser or forklift.service_company.user == datauser)):
               return True
         return False
      
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context

class TransmissionModelCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = TransmissionModelForm
   model = TransmissionModel
   template_name = 'forklift/transmission_model_edit.html'
   permission_required = 'forklift.add_transmissionmodel'

class TransmissionModelUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = TransmissionModelForm
   model = TransmissionModel
   template_name = 'forklift/transmission_model_edit.html'
   permission_required = 'forklift.change_transmissionmodel'

class TransmissionModelDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   form_class = TransmissionModelForm
   model = TransmissionModel
   template_name = 'forklift/transmission_model_delete.html'
   permission_required = 'forklift.delete_transmissionmodel'



#Ведущий мост
class DriveAxleModelDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = DriveAxleModel
   template_name = 'forklift/drive_axle_model.html'
   context_object_name = 'drive_axle_model'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         forklifts = Forklift.objects.all()
         for forklift in forklifts:
            drive_axle_model = forklift.drive_axle_model
            if(self.get_object() == drive_axle_model and (forklift.client.user == datauser or forklift.service_company.user == datauser)):
               return True
         return False
      
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context

class DriveAxleModelCreate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = DriveAxleModelForm
   model = DriveAxleModel
   template_name = 'forklift/drive_axle_model_edit.html'
   permission_required = 'forklift.add_driveaxlemodel'

class DriveAxleModelUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = DriveAxleModelForm
   model = DriveAxleModel
   template_name = 'forklift/drive_axle_model_edit.html'
   permission_required = 'forklift.change_driveaxlemodel'
      
class DriveAxleModelDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   form_class = DriveAxleModelForm
   model = DriveAxleModel
   template_name = 'forklift/drive_axle_model_delete.html'
   permission_required = 'forklift.delete_driveaxlemodel'



#Управляемый мост
class ControlledBridgeModelDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = ControlledBridgeModel
   template_name = 'forklift/controlled_bridge_model.html'
   context_object_name = 'controlled_bridge_model'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         forklifts = Forklift.objects.all()
         for forklift in forklifts:
            controlled_bridge_model = forklift.controlled_bridge_model
            if(self.get_object() == controlled_bridge_model and (forklift.client.user == datauser or forklift.service_company.user == datauser)):
               return True
         return False
      
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context

class ControlledBridgeModelCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = ControlledBridgeModelForm
   model = ControlledBridgeModel
   template_name = 'forklift/controlled_bridge_model_edit.html'
   permission_required = 'forklift.add_controlledbridgemodel'

class ControlledBridgeModelUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = ControlledBridgeModelForm
   model = ControlledBridgeModel
   template_name = 'forklift/controlled_bridge_model_edit.html'
   permission_required = 'forklift.change_controlledbridgemodel'

class ControlledBridgeModelDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   form_class = ControlledBridgeModelForm
   model = ControlledBridgeModel
   template_name = 'forklift/controlled_bridge_model_delete.html'
   permission_required = 'forklift.delete_controlledbridgemodel'



#Рекламации
class ClaimList(LoginRequiredMixin, ListView, ClaimListMixin):
    model = Claim
    template_name = 'forklift/claims.html'
    context_object_name = 'claim'
    permission_required = 'forklift.view_claim'


    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = ClaimFilter(self.request.GET, queryset)
       return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['filterset'] = self.filterset
       return context
    
class ClaimDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Claim
    template_name = 'forklift/claim.html'
    context_object_name = 'claim'
    permission_required = 'forklift.view_claim'

    def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.forklift.client.user == datauser or obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       user_in_group_service_company = self.request.user.groups.filter(name='service_company').exists()
       context['user_in_group_service_company'] = user_in_group_service_company
       return context

class ClaimCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = ClaimForm
   model = Claim
   template_name = 'forklift/claim_edit.html'
   permission_required = 'forklift.add_claim'

class ClaimUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
   form_class = ClaimForm
   model = Claim
   template_name = 'forklift/claim_edit.html'
   permission_required = 'forklift.change_claim'

   def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()

class ClaimDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = Claim
   template_name = 'forklift/claim_delete.html'
   success_url = reverse_lazy('claim_list')
   permission_required = 'forklift.delete_claim'

   def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()


#Характер отказа
class NatureRefusalDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = NatureRefusal
   template_name = 'forklift/nature_failure.html'
   context_object_name = 'nature_failure'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         claims = Claim.objects.all()
         for claim in claims:
            nature_failure = claim.order_note
            if(self.get_object() == nature_failure and (claim.car.client.user == datauser or claim.service_company.user == datauser)):
               return True
         return False
      
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context
      
class NatureRefusalCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = NatureRefusalForm
   model = NatureRefusal
   template_name = 'forklift/nature_failure_edit.html'
   permission_required = 'forklift.add_NatureRefusal'

class NatureRefusalUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = NatureRefusalForm
   model = NatureRefusal
   template_name = 'forklift/nature_failure_edit.html'
   permission_required = 'forklift.change_NatureRefusal'

class NatureRefusalDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   form_class = NatureRefusalForm
   model = NatureRefusal
   template_name = 'forklift/nature_failure_delete.html'
   permission_required = 'forklift.delete_NatureRefusal'



#Способ восстановления
class RecoveryMethodDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = RecoveryMethod
   template_name = 'forklift/recovery_method.html'
   context_object_name = 'recovery_method'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         claims = Claim.objects.all()
         for claim in claims:
            recovery_method = claim.recovery_method
            if(self.get_object() == recovery_method and (claim.car.client.user == datauser or claim.service_company.user == datauser)):
               return True
         return False
      
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context
      
class RecoveryMethodCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   form_class = RecoveryMethodForm
   model = RecoveryMethod
   template_name = 'forklift/recovery_method_edit.html'
   permission_required = 'forklift.add_recoverymethod'

class RecoveryMethodUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   form_class = RecoveryMethodForm
   model = RecoveryMethod
   template_name = 'forklift/recovery_method_edit.html'
   permission_required = 'forklift.change_recoverymethod'

class RecoveryMethodDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   form_class = RecoveryMethodForm
   model = RecoveryMethod
   template_name = 'forklift/recovery_method_delete.html'
   permission_required = 'forklift.delete_recoverymethod'



#Клиенты
class ClientDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = Client
   template_name = 'forklift/client.html'
   context_object_name = 'client'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         forklifts = Forklift.objects.all()
         for forklift in forklifts:
            client = forklift.client
            if(self.get_object() == client and (forklift.client.user == datauser or forklift.service_company.user == datauser)):
               return True
         return False



#Сервисные компании
class ServiceCompanyDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = Service_Company
   template_name = 'forklift/service_company.html'
   context_object_name = 'service_company'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_superuser or datauser.groups.filter(name='manager').exists()):
         return True
      else:
         forklifts = Forklift.objects.all()
         for forklift in forklifts:
            service_company = forklift.service_company
            if(self.get_object() == service_company and (forklift.client.user == datauser or forklift.service_company.user == datauser)):
               return True
         return False