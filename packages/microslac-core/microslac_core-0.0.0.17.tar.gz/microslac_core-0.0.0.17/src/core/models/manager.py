from django.db.models import Manager

from core.models.queryset import BaseQuerySet


class BaseManager(Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)
