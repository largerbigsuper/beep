from django.db.models.manager import Manager
from django.core.cache import cache


class ModelManager(Manager):
    
    cache = cache
