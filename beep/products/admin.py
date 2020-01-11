from django.contrib import admin

from beep.users.models import mm_Point
from .models import (Sku, SkuOrderItem, mm_SkuOrderItem, 
                    SkuType, mm_SkuType, 
                    SkuPropertyName, mm_SkuPropertyName,
                    SkuProperty, mm_SkuProperty,
                    SkuOrderAddress, mm_SkuOrderAddress
                    )
from .forms import SkuAdminForm, SkuPropertyForm

class SkuPropertyInline(admin.TabularInline):
    model = SkuProperty
    form = SkuPropertyForm
    extra = 0


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    form = SkuAdminForm

    list_display = ['id', 'name', 'cover', 'point', 'detail', 'total_left', 'create_at']
    search_fields = ['name']
    ordering = ['order_num', '-create_at']
    inlines = [SkuPropertyInline]


def make_sku_exchange_done(modeladmin, request, queryset):
    """审核通过
    """
    queryset.update(status=mm_SkuOrderItem.STATUS_DONE)

make_sku_exchange_done.short_description = '审核通过'

def make_sku_exchange_refound(modeladmin, request, queryset):
    """退回积分
    """
    for obj in queryset:
        mm_Point.add_action(obj.user_id, action=mm_Point.ACTION_SKU_EXCHANGE_REFOUND, amount=obj.point)
        obj.status = mm_SkuOrderItem.STATUS_REFUSED
        obj.save()

make_sku_exchange_refound.short_description = '审核拒绝'

@admin.register(SkuOrderItem)
class SkuOrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'sku', 'point', 'create_at', 'status']
    list_filter = ['status']
    search_fields = ['user']
    actions = [make_sku_exchange_done, make_sku_exchange_refound]


@admin.register(SkuType)
class SkuTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(SkuPropertyName)
class SkuPropertyNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(SkuProperty)
class SkuPropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku', 'property_name_1', 'property_value_1', 
    'property_name_2', 'property_value_2', 'property_name_3', 'property_value_3',
    'total_left', 'total_sales', 'update_at']

    form = SkuPropertyForm


@admin.register(SkuOrderAddress)
class SkuOrderAddressAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'user', 'name', 'phone', 'detail', 'update_at']