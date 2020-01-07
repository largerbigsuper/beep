from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Sku

class SkuAdminForm(forms.ModelForm):

    class Meta:
        model = Sku
        fields = '__all__'
        widgets = {
            'detail': CKEditorUploadingWidget(),
        }
