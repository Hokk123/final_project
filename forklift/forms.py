from django import forms
from .models import *


class ForkliftForm(forms.ModelForm):
   class Meta:
       model = Forklift
       fields = [
           'machine_serial_number',
           'model_equipment',
           'engine_model',
           'engine_serial_number',
           'transmission_model',
           'transmission_serial_number',
           'drive_axle_model',
           'drive_axle_serial_number',
           'controlled_bridge_model',
           'controlled_bridge_serial_number',
           'delivery_contract',
           'date_of_shipment',
           'end_user',
           'delivery_address',
           'equipment',
           'client',
           'service_company',
       ]
    
   def __init__(self, *args, **kwargs):
       user = kwargs.pop('user', None)
       super(ForkliftForm, self).__init__(*args, **kwargs)

       if user and not user.is_authenticated:
           self.fields['delivery_contract'].widget.attrs['disabled'] = True
           self.fields['date_of_shipment'].widget.attrs['disabled'] = True
           self.fields['end_user'].widget.attrs['disabled'] = True
           self.fields['delivery_address'].widget.attrs['disabled'] = True
           self.fields['equipment'].widget.attrs['disabled'] = True
           self.fields['client'].widget.attrs['disabled'] = True
           self.fields['service_company'].widget.attrs['disabled'] = True

class ToForm(forms.ModelForm):
    class Meta:
        model = To
        fields = [
           'type',
           'date',
           'operating',
           'orders_number',
           'orders_date',
           'organization',
           'car',
           'service_company',
        ]

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            'orders_date',
            'operating',
            'order_note',
            'order_description',
            'recovery_method',
            'used_spare_parts',
            'recovery_date',
            'downtime',
            'car',
            'service_company',
        ]

class ModelEquipmentForm(forms.ModelForm):
    class Meta:
        model = ModelEquipment
        fields = [
            'title',
            'description',
        ]

class EngineModelForm(forms.ModelForm):
    class Meta:
        model = EngineModel
        fields = [
            'title',
            'description',
        ]

class TransmissionModelForm(forms.ModelForm):
    class Meta:
        model = TransmissionModel
        fields = [
            'title',
            'description',
        ]

class DriveAxleModelForm(forms.ModelForm):
    class Meta:
        model = DriveAxleModel
        fields = [
            'title',
            'description',
        ]

class ControlledBridgeModelForm(forms.ModelForm):
    class Meta:
        model = ControlledBridgeModel
        fields = [
            'title',
            'description',
        ]

class TypeToForm(forms.ModelForm):
    class Meta:
        model = TypeTo
        fields = [
            'title',
            'description',
        ]

class NatureRefusalForm(forms.ModelForm):
    class Meta:
        model = NatureRefusal
        fields = [
            'title',
            'description',
        ]

class RecoveryMethodForm(forms.ModelForm):
    class Meta:
        model = EngineModel
        fields = [
            'title',
            'description',
        ]