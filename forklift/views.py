from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import *
from .filters import CarsFilter, ToFilter, ClaimFilter


class CarsList(LoginRequiredMixin, ListView):
    #указываем модель, объекты которой мы будем выводить
    model = Forklift
    # form_class = CarForm
    # #поле, которое будет использоваться для сортировки объектов
    ordering = '-date_of_shipment'
    #указываем имя шаблона, в котором будут все инструкции о том
    #как именно пользователю должны быть показаны наши объекты
    template_name = 'info/cars.html'
    #это имя списка, в котором будут лежать все объекты.
    #его надо указать, чтобы обратиться к списку объекту в html-шаблоне.
    context_object_name = 'cars'


    # Переопределяем функцию получения списка машин
    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = CarsFilter(self.request.GET, queryset)
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

class CarDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    #Модель все та же, но мы хотим получать информацию по отдельному товару
    model = Forklift
    #Используем другой шаблон - car.html
    template_name = 'info/car.html'
    #Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'car'
    permission_required = ('info.view_car', )

    def test_func(self):
       obj = self.get_object()
       ruser = self.request.user
       return obj.client.user == ruser or obj.service_company.user == ruser or ruser.is_superuser or ruser.groups.filter(name='manager').exists()
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       #проверяем принадлежность пользователя к группе для отображения кнопки создания машины
       user_in_group_manager = self.request.user.groups.filter(name='manager').exists()
       context['user_in_group_manager'] = user_in_group_manager
       return context