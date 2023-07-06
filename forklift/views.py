from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import *

from .models import *
from .filters import ForkliftFilter, ToFilter, ClaimFilter


class ForkliftsList(LoginRequiredMixin, ListView):
    #указываем модель, объекты которой мы будем выводить
    model = Forklift
    # form_class = forkliftForm
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



class ToList(LoginRequiredMixin, ListView):
    model = To
    #template_name = 'forklift/to.html'
    template_name = 'forklift/forklifts.html'
    context_object_name = 'to'
    permission_required = 'forklift.view_to'


    # Переопределяем функцию получения списка машин
    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = ToFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список машин
       return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       context['ordering'] = self.ordering
       return context

class ToDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    #Модель все та же, но мы хотим получать информацию по отдельному товару
    model = To
    #Используем другой шаблон - forklift.html
    template_name = 'forklift/to.html'
    #Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'to'
    permission_required = 'forklift.view_to'
    
    def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.forklift.client.user == datauser or obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()

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
       return obj.forklift.client.user == datauser or obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()

class ToDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = To
   template_name = 'forklift/to_delete.html'
   success_url = reverse_lazy('to_list')
   permission_required = 'forklift.delete_to'

   def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.forklift.client.user == datauser or obj.service_company.user == datauser or datauser.is_superuser or datauser.groups.filter(name='manager').exists()



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
            if(self.get_object() == controlled_bridge_model and (forklift.client.user == ruser or forklift.service_company.user == ruser)):
               return True
         return False
      
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context


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