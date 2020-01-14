from datetime import datetime
from random import random

from django.db import models
from django.db.models import F
from django.conf import settings

from utils.modelmanager import ModelManager


class SkuTypeManager(ModelManager):
    pass

class SkuType(models.Model):
    
    name = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='类型')
    objects = SkuTypeManager()
    class Meta:
        db_table = 'beep_sku_type'
        ordering = ['-id']
        verbose_name = '商品类型'
        verbose_name_plural = '商品类型'

    def __str__(self):
        return self.name

mm_SkuType = SkuType.objects

class SkuManager(ModelManager):

    STATUS_EDITING = 0
    STATUS_PUBLISHED = 1
    STATUS_RECALL = 2

    STATUS_CHOICES = [
        (STATUS_EDITING, '编辑中'),
        (STATUS_PUBLISHED, '已上架'),
        (STATUS_RECALL, '已下架')
    ]

    def published_sku(self):
        """在售商品
        """
        return self.filter(status=self.STATUS_PUBLISHED)
    
    def recommand_sku(self):
        """推荐商品
        """
        return self.published_sku().filter(is_recommand=True)

    def update_data(self, pk, field_name, amount=1):
        if amount > 0: 
            value = F(field_name) + amount
        else:
            value = F(field_name) - abs(amount)
        updates = {
            field_name: value
        }
        self.filter(pk=pk).update(**updates)

class Sku(models.Model):
    """积分商品
    """
    sku_type = models.ForeignKey(SkuType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='类型')
    name = models.CharField(max_length=120, verbose_name='商品名')
    cover = models.ImageField(verbose_name='封面图')
    point = models.PositiveIntegerField(default=0, verbose_name='所需积分')
    detail = models.TextField(default='', blank=True, verbose_name='详情')
    total_left = models.PositiveIntegerField(default=0, blank=True, verbose_name='总量')
    total_sales = models.PositiveIntegerField(default=0, blank=True, verbose_name='销量')
    status = models.PositiveSmallIntegerField(choices=SkuManager.STATUS_CHOICES,
                                            default=SkuManager.STATUS_EDITING,
                                            verbose_name='兑换商品状态')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    order_num = models.IntegerField(default=10000, verbose_name='排序值[越小越靠前]')
    is_recommand = models.BooleanField(default=False, blank=True, verbose_name='推荐')
    
    objects = SkuManager()

    class Meta:
        db_table = 'beep_sku'
        ordering = ['order_num', '-create_at']
        verbose_name  = '商品'
        verbose_name_plural  = '商品'

    def __str__(self):
        return self.name

mm_Sku = Sku.objects

class SkuPropertyNameManager(ModelManager):
    pass

class SkuPropertyName(models.Model):
    """商品属性名称
    """
    
    name = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='属性名称')

    objects = SkuPropertyNameManager()

    class Meta:
        db_table = 'beep_sku_property_name'
        ordering = ['-id']
        verbose_name = '商品属性名'
        verbose_name_plural = '商品属性名'


mm_SkuPropertyName = SkuPropertyName.objects

class SkuPropertyManager(ModelManager):
    pass


class SkuProperty(models.Model):
    """商品属性
    """
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name='sku_properties', verbose_name='商品')
    property_name_1 = models.CharField(max_length=20, verbose_name='属性名')
    property_value_1 = models.CharField(max_length=20, verbose_name='属性值')
    property_name_2 = models.CharField(max_length=20, null=True, blank=True, verbose_name='属性名2')
    property_value_2 = models.CharField(max_length=20, null=True, blank=True, verbose_name='属性值2')
    property_name_3 = models.CharField(max_length=20, null=True, blank=True, verbose_name='属性名3')
    property_value_3 = models.CharField(max_length=20,null=True, blank=True, verbose_name='属性值3')
    total_left = models.PositiveIntegerField(default=0, blank=True, verbose_name='总量')
    total_sales = models.PositiveIntegerField(default=0, blank=True, verbose_name='销量')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = SkuPropertyManager()

    class Meta:
        db_table = 'beep_sku_property'
        ordering = ['-id']
        verbose_name = '商品属性'
        verbose_name_plural = '商品属性'

    def __str__(self):
        descprition = self.property_name_1 + ': ' + self.property_value_1 + ' '
        if self.property_name_2 and self.property_value_2:
            descprition += self.property_name_2 + ': ' + self.property_value_2 + ' '
        if self.property_name_3 and self.property_value_3:
            descprition += self.property_name_3 + ': ' + self.property_value_3 + ' '
        return descprition
 
mm_SkuProperty = SkuProperty.objects


class SkuOrderAddressManager(ModelManager):
    
    def my_address(self, user_id):
        """我的收货地址
        """
        return self.exclude(is_del=True).filter(user_id=user_id)

class SkuOrderAddress(models.Model):
    """用户收货地址
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    name = models.CharField(max_length=20, verbose_name='收件人')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    detail = models.CharField(max_length=200, verbose_name='详细地址')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_del = models.BooleanField(default=False, verbose_name='已删除')

    objects = SkuOrderAddressManager()

    class Meta:
        db_table = 'beep_sku_order_address'
        ordering = ['-id']
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址'
    
    def __str__(self):
        return '用户名：' + self.user.name + ' ' + '收件人：' + self.name + ' ' + '手机号：' + self.phone + ' '+ '详细地址：' + self.detail

mm_SkuOrderAddress = SkuOrderAddress.objects

class SkuOrderManager(ModelManager):
    STATUS_SUBMITED = 0
    STATUS_VERFIED = 1
    STATUS_PROCESSING = 2
    STATUS_DONE = 3
    STATUS_REFUSED = 4

    STATUS_ORDER = (
        (STATUS_SUBMITED, '已提交'),
        (STATUS_VERFIED, '审核通过'),
        (STATUS_PROCESSING, '审核通过，正在处理'),
        (STATUS_DONE, '已完成'),
        (STATUS_REFUSED, '审核拒绝'),
    )

    def get_order_num(self):
        datetime_prefix = datetime.now().strftime('%Y%m%d%H%M%S%f')
        random_suffix = str(random())[-8:]
        order_num = datetime_prefix + random_suffix
        return order_num

    def my_orders(self, user_id):
        return self.exclude(user_del=True).filter(user_id=user_id)

class SkuOrder(models.Model):

    order_num = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='订单号')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    point = models.PositiveIntegerField(default=0, verbose_name='消耗积分')
    address = models.ForeignKey(SkuOrderAddress, null=True, on_delete=models.CASCADE, verbose_name='地址信息')
    status = models.PositiveIntegerField(choices=SkuOrderManager.STATUS_ORDER,
                                            default=SkuOrderManager.STATUS_SUBMITED,
                                            verbose_name='申请状态')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    user_del = models.BooleanField(default=False, verbose_name='已删除[用户]')
    objects = SkuOrderManager()

    class Meta:
        db_table = 'beep_sku_order'
        ordering = ['-create_at']
        verbose_name  = '订单'
        verbose_name_plural  = '订单'

    def __str__(self):
        return self.order_num

mm_SkuOrder = SkuOrder.objects


class SkuOrderItemManager(ModelManager):
    
    STATUS_SUBMITED = 0
    STATUS_VERFIED = 1
    STATUS_PROCESSING = 2
    STATUS_DONE = 3
    STATUS_REFUSED = 4

    STATUS_ORDER = (
        (STATUS_SUBMITED, '已提交'),
        (STATUS_VERFIED, '审核通过'),
        (STATUS_PROCESSING, '审核通过，正在处理'),
        (STATUS_DONE, '已完成'),
        (STATUS_REFUSED, '审核拒绝'),
    )

    def add_exchange(self, user_id, sku_id, point):
        """增加记录
        """
        return self.create(user_id=user_id, sku_id=sku_id, point=point)

class SkuOrderItem(models.Model):
    """兑换申请记录
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, verbose_name='积分商品')
    sku_property = models.ForeignKey(SkuProperty, null=True, on_delete=models.CASCADE, verbose_name='商品属性')
    quantity = models.PositiveIntegerField(default=1, verbose_name='购买数量')
    order = models.ForeignKey(SkuOrder, null=True, related_name='sku_order_items',on_delete=models.CASCADE, verbose_name='订单')
    point = models.PositiveIntegerField(default=0, verbose_name='消耗积分')
    status = models.PositiveIntegerField(choices=SkuOrderItemManager.STATUS_ORDER,
                                        default=SkuOrderItemManager.STATUS_SUBMITED,
                                        verbose_name='申请状态')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = SkuOrderItemManager()

    class Meta:
        db_table = 'beep_sku_order_item'
        ordering = ['-create_at']
        verbose_name  = '兑换申请'
        verbose_name_plural  = '兑换申请'

mm_SkuOrderItem = SkuOrderItem.objects


class SkuCartManager(ModelManager):
    
    def my_skucart(self, user_id):
        return self.filter(user_id=user_id)

    def add_sku(self, user_id, sku_id, sku_property_id, quantity):
        params = {
            'user_id': user_id,
            'sku_id': sku_id,
            'sku_property_id': sku_property_id
        }
        obj = self.filter(**params).first()
        if obj:
            obj.quantity += quantity
            obj.save()
        else:
            obj = self.create(quantity=quantity, **params)
        return obj

class SkuCart(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, verbose_name='商品')
    sku_property = models.ForeignKey(SkuProperty, on_delete=models.CASCADE, verbose_name='商品属性')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    objects = SkuCartManager()

    class Meta:
        db_table = 'beep_sku_cart'
        ordering = ['-create_at']
        unique_together = ['user', 'sku', 'sku_property']
        verbose_name = '购物车'
        verbose_name_plural = '购物车'

mm_SkuCart = SkuCart.objects
