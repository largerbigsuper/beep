from django.contrib import admin

from .models import News, CrawledDocument

class NewsAdmin(admin.ModelAdmin):
    pass


admin.site.register(News, NewsAdmin)

@admin.register(CrawledDocument)
class CrawledDocumentAdmin(admin.ModelAdmin):
    
    list_display = [f.name for f in CrawledDocument._meta.get_fields()]
