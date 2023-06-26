from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class ModelEquipment(models.Model): #модель техники (справочник)
    title = models.CharField(max_length = 32)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    

class EngineModel(models.Model):  #модель двигателя (справочник)
    title = models.CharField(max_length = 32)
    description = models.TextField()
    
    def __str__(self):
        return self.title


class TransmissionModel(models.Model):  #модель трансмиссии (справочник)
    title = models.CharField(max_length = 32)
    description = models.TextField()
    
    def __str__(self):
        return self.title


class DriveAxleModel(models.Model):  #модель ведущего моста (справочник)
    title = models.CharField(max_length = 32)
    description = models.TextField()
    
    def __str__(self):
        return self.title


class ControlledBridgeModel(models.Model):  #модель управляемого моста (справочник)
    title = models.CharField(max_length = 32)
    description = models.TextField()
    
    def __str__(self):
        return self.title


class TypeTo(models.Model):  #вид ТО (справочник)
    title = models.CharField(max_length = 32)
    description = models.TextField()
    
    def __str__(self):
        return self.title


class NatureRefusal(models.Model):  #характер отказа
    title = models.CharField(max_length = 32)
    description = models.TextField()
    
    def __str__(self):
        return self.title


class RecoveryMethod(models.Model):  #способ восстановления
    title = models.CharField(max_length = 32)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    

class Service_Company(models.Model):  #справочник пользователей с соответствующими правами
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 50)
    description = models.TextField()
    
    def __str__(self):
        return self.title


class Client(models.Model):  #справочник пользователей с соответствующими правами
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'user_client')
    title = models.CharField(max_length = 50)
    description = models.TextField()
    
    def __str__(self):
        return self.title



class Forklift(models.Model):  #вилочный погрузчик
    machine_serial_number = models.CharField(max_length = 32) #заводской № машины
    model_equipment = models.ForeignKey(ModelEquipment, on_delete = models.CASCADE) #модель машины
    engine_model = models.ForeignKey(EngineModel, on_delete = models.CASCADE) #модель двигателя
    engine_serial_number = models.CharField(max_length = 32) #заводской № двигателя
    transmission_model = models.ForeignKey(TransmissionModel, on_delete = models.CASCADE) #модель трансмиссии
    transmission_serial_number = models.CharField(max_length = 32) #заводской № трансмиссии
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete = models.CASCADE) #модель ведущего моста
    drive_axle_serial_number = models.CharField(max_length = 32) #заводской № ведущего моста
    controlled_bridge_model = models.ForeignKey(ControlledBridgeModel, on_delete = models.CASCADE) #модель управляемого моста
    controlled_bridge_serial_number = models.CharField(max_length = 32) #заводской № управляемого моста
    delivery_contract = models.CharField(max_length = 32) #договор поставки №, дата
    date_of_shipment = models.DateField() #дата отгрузки с завода
    end_user = models.CharField(max_length = 64) #грузополучатель
    delivery_address = models.CharField(max_length = 256) #адрес поставки
    equipment = models.CharField(max_length = 256) #комплектация
    client = models.ForeignKey(Client, on_delete = models.CASCADE) #клиент
    service_company = models.ForeignKey(Service_Company, on_delete = models.CASCADE) #сервисная компания
    
    def get_absolute_url(self):
        return reverse('cars_list', args = [str(self.id)])
    
    def __str__(self):
        return self.machine_serial_number


class To(models.Model): #TO
    type = models.ForeignKey(TypeTo, on_delete = models.CASCADE) #вид ТО
    date = models.DateField() #дата проведения ТО
    operating = models.PositiveIntegerField(default = 0) #наработка, м/час
    orders_number = models.CharField(max_length = 32) #№ заказ-наряда
    orders_date = models.DateField() #дата заказ-наряда
    organization = models.CharField(max_length = 32) #организация, проводившая ТО
    car = models.ForeignKey(Forklift, on_delete = models.CASCADE) #машина (база данных машин)
    service_company = models.ForeignKey(Service_Company, on_delete = models.CASCADE) #сервисная компания
    
    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('to_detail', args = [str(self.id)])
    
    def __str__(self):
        return self.orders_number
    

class Claim(models.Model):  #рекламация
    orders_date = models.DateField() #дата отказа
    operating = models.PositiveIntegerField(default = 0) #наработка, м/час
    order_note = models.ForeignKey(NatureRefusal, on_delete = models.CASCADE) #узел отказа
    order_description = models.TextField() #описание отказа
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete = models.CASCADE) #способ восстановления
    used_spare_parts = models.TextField() #используемые запасные части
    recovery_date = models.DateField() #дата восстановления
    downtime = models.IntegerField(default = 0) #время простоя техники
    car = models.ForeignKey(Forklift, on_delete = models.CASCADE) #машина (база данных машин)
    service_company = models.ForeignKey(Service_Company, on_delete = models.CASCADE) #сервисная компания

    class Meta:
        ordering = ['-orders_date']

    def get_absolute_url(self):
        return reverse('claim_detail', args = [str(self.id)])
    
    def __str__(self):
        return self.order_description
    



