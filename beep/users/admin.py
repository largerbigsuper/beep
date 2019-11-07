from django import forms
from django.contrib import admin
from django.contrib.auth import models, password_validation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext, gettext_lazy as _


from .models import User

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ("name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def _post_clean(self):
        super()._post_clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data['account']
        if commit:
            user.save()
        return user


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = UserCreationForm

    parent_fields = {f.name for f in models.User._meta.fields}
    extra_fields = {f.name for f in User._meta.fields} - {f.name for f in models.User._meta.fields}
    extra_fields.remove('create_at')
    extra_fields.remove('update_at')
    
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': tuple(extra_fields)}),
    )

    list_display = ['id', 'name', 'account', 'gender', 'avatar_url', 'label_type']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account', 'name', 'avatar_url', 'password1'),
        }),
    )

admin.site.register(User, MyUserAdmin)
