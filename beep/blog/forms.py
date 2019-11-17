from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget

from .models import Blog_Article
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class Blog_ArticleAdminForm(forms.ModelForm):
    
    class Meta:
        model = Blog_Article
        fields = '__all__'
        widgets = {
            'content': CKEditorUploadingWidget(),
        }
