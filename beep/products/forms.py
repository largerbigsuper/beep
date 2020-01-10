from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms.widgets import Select

from .models import Sku, SkuProperty, mm_SkuPropertyName

class SkuAdminForm(forms.ModelForm):

    class Meta:
        model = Sku
        fields = '__all__'
        widgets = {
            'detail': CKEditorUploadingWidget(),
        }

class SkuPropertyForm(forms.ModelForm):

    class Meta:
        model = SkuProperty
        fields = '__all__'
        CHOICES = mm_SkuPropertyName.all()
        choices = tuple(((x.name, x.name) for x in CHOICES))
        choices_2 = tuple([(None, None)] + list(choices))
        choices_3 = tuple([(None, None)] + list(choices))

        widgets = {
            'property_name_1': Select(choices=choices),
            'property_name_2': Select(choices=choices_2),
            'property_name_3': Select(choices=choices_3),
        }
