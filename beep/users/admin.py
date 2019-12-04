from django import forms
from django.contrib import admin
from django.contrib.auth import models, password_validation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.html import mark_safe

from .models import User, mm_User, LableApply, mm_LableApply

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
    ordering = ('-id', )

    user_info = ('name', 'age', 'gender', 'desc', 'email', 'mini_openid', 'openid', 'unionid', 'avatar_url')
    data_info = ('total_blog', 'total_following', 'total_followers', 'label_type')
    user_info_tuple = user_info + data_info 
    fieldsets = (
        (None, {'fields': ('account', 'password')}),
        (_('Personal info'), {'fields': user_info_tuple}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ['id', 'name', 'account', 'gender', 'avatar_url', 'label_type']
    search_fields = ['name', 'account']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account', 'name', 'avatar_url', 'password1'),
        }),
    )

admin.site.register(User, MyUserAdmin)



def make_apply_passed(modeladmin, request, queryset):
    """设置通过申请
    """
    queryset.update(status=mm_LableApply.STATUS_PASSED)
    for record in queryset:
        record.user.label_type = record.lebel_type
        record.user.save()

make_apply_passed.short_description = '审核通过'

def make_apply_failed(modeladmin, request, queryset):
    """设置通过申请失败
    """
    queryset.update(status=mm_LableApply.STATUS_PASSED)

make_apply_failed.short_description = '审核失败'


@admin.register(LableApply)
class LableApplyAdmin(admin.ModelAdmin):

    list_display = ['user', 'lebel_type', 'image_tag', 'desc', 'status', 'create_at']
    list_filter = ['lebel_type', 'status']
    # list_editable = ['status']
    search_fields = ['user__account']
    actions = [make_apply_passed, make_apply_failed]
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(obj.image))

    image_tag.short_description = '图片'
