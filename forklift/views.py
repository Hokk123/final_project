from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

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
    #Модель все та же, но мы хотим получать информацию по отдельному товару
    model = Forklift
    #Используем другой шаблон - forklift.html
    template_name = 'forklift/forklift.html'
    #Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'forklift'
    permission_required = ('forklift.view_forklift', )

    def test_func(self):
       obj = self.get_object()
       datauser = self.request.user
       return obj.client.user == datauser or obj.service_company.user == datauser or datauser.is_supedatauser or datauser.groups.filter(name='manager').exists()
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context


class ModelEquipmentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
   model = ModelEquipment
   template_name = 'forklift/model_equipment.html'
   context_object_name = 'model_equipment'

   def test_func(self):
      datauser = self.request.user
      if(datauser.is_supedatauser or datauser.groups.filter(name='manager').exists()):
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