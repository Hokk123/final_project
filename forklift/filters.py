from django_filters import FilterSet
from .models import Forklift, To, Claim


# фильтр для модели погрузчик
class CarsFilter(FilterSet):
    class Meta:
        model = Forklift
        fields = {
            'machine_serial_number' : ['icontains'],
            'model_equipment__title': ['icontains'],
            'engine_model__title': ['icontains'],
            'transmission_model__title': ['icontains'],
            'drive_axle_model__title': ['icontains'],
            'controlled_bridge_model__title': ['icontains'],
        }

# фильтр для модели TO
class ToFilter(FilterSet):
    class Meta:
        model = To
        fields = {
            'type__title': ['icontains'],
            'car__machine_serial_number': ['icontains'],
            'service_company__title': ['icontains'],
        }

# фильтр для модели рекламация
class ClaimFilter(FilterSet):
    class Meta:
        model = Claim
        fields = {
            'order_note__title': ['icontains'],
            'recovery_method__title': ['icontains'],
            'service_company__title': ['icontains'],
        }