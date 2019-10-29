from django.contrib import admin

from .models import Activity, Registration

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'cover', 'activity_type', 'start_at', 'end_at']

admin.site.register(Activity, ActivityAdmin)

class RegistrationAdmin(admin.ModelAdmin):

    pass

admin.site.register(Registration, RegistrationAdmin)
