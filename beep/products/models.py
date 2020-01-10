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

    def update_count_data(self, pk):
        """更新剩余数量与销量
        """
        self.filter(pk=pk).update(total_left=F('total_left') - 1, total_sales=F('total_sales') + 1)

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
    
    objects = SkuManager()

    class Meta:
        db_table = 'beep_sku'
        ordering = ['order_num', '-create_at']
        verbose_name  = '兑换商品'
        verbose_name_plural  = '兑换商品'

    def __str__(self):
        return self.name



mm_Sku = Sku.objects


class SkuExchangeManager(ModelManager):
    
    STATUS_SUBMITED = 0
    STATUS_DONE = 1
    STATUS_REFUSED = 2

    STATUS_EXCHANGE = (
        (STATUS_SUBMITED, '已提交'),
        (STATUS_DONE, '审核通过'),
        (STATUS_REFUSED, '审核拒绝'),
    )

    def add_exchange(self, user_id, sku_id, point):
        """增加记录
        """
        return self.create(user_id=user_id, sku_id=sku_id, point=point)

class SkuExchange(models.Model):
    """兑换申请记录
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, verbose_name='积分商品')
    point = models.PositiveIntegerField(default=0, verbose_name='消耗积分')
    status = models.PositiveIntegerField(choices=SkuExchangeManager.STATUS_EXCHANGE,
                                        default=SkuExchangeManager.STATUS_SUBMITED,
                                        verbose_name='申请状态')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = SkuExchangeManager()

    class Meta:
        db_table = 'beep_sku_exchange'
        ordering = ['-create_at']
        verbose_name  = '兑换申请'
        verbose_name_plural  = '兑换申请'

mm_SkuExchange = SkuExchange.objects



class SkuPropertyNameManager(ModelManager):
    pass

class SkuPropertyName(models.Model):
    """商品属性名称
    """
    
    name = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='熟悉名称')

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

mm_SkuProperty = SkuProperty.objects