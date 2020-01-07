from django.contrib import admin

from beep.users.models import mm_Point
from .models import Sku, SkuExchange, mm_SkuExchange
from .forms import SkuAdminForm

@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    form = SkuAdminForm

    list_display = ['id', 'name', 'cover', 'point', 'detail', 'total_left', 'create_at']
    search_fields = ['name']
    ordering = ['order_num', '-create_at']


def make_sku_exchange_done(modeladmin, request, queryset):
    """审核通过
    """
    queryset.update(status=mm_SkuExchange.STATUS_DONE)

make_sku_exchange_done.short_description = '审核通过'

def make_sku_exchange_refound(modeladmin, request, queryset):
    """退回积分
    """
    for obj in queryset:
        mm_Point.add_action(obj.user_id, action=mm_Point.ACTION_SKU_EXCHANGE_REFOUND, amount=obj.point)
        obj.status = mm_SkuExchange.STATUS_REFUSED
        obj.save()

make_sku_exchange_refound.short_description = '审核拒绝'

@admin.register(SkuExchange)
class SkuExchangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'sku', 'point', 'create_at', 'status']
    list_filter = ['status']
    search_fields = ['user']
    actions = [make_sku_exchange_done, make_sku_exchange_refound]