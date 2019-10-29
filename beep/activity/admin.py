from django.contrib import admin

from .models import Activity, Registration

class ActivityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Activity, ActivityAdmin)

class RegistrationAdmin(admin.ModelAdmin):

    pass

admin.site.register(Registration, RegistrationAdmin)
