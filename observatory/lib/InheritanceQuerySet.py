from django.db.models.query import QuerySet
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.core.exceptions import ObjectDoesNotExist

class InheritanceQuerySet(QuerySet):
  def select_subclasses(self, *subclasses):
    if not subclasses:
      subclasses = [o for o in dir(self.model)
              if isinstance(getattr(self.model, o), SingleRelatedObjectDescriptor)\
              and issubclass(getattr(self.model,o).related.model, self.model)]
    new_qs = self.select_related(*subclasses)
    new_qs.subclasses = subclasses
    return new_qs

  def _clone(self, klass=None, setup=False, **kwargs):
    try:
      kwargs.update({'subclasses': self.subclasses})
    except AttributeError:
      pass
    return super(InheritanceQuerySet, self)._clone(klass, setup, **kwargs)

  def _get_subclasses(self, obj):
    result = []
    for s in getattr(self, 'subclassses', []):
        try:
            if getattr(obj, s):
                result += getattr(obj, s)
        except ObjectDoesNotExist:
            continue
    return result or [obj]


  def iterator(self):
    iter = super(InheritanceQuerySet, self).iterator()
    if getattr(self, 'subclasses', False):
      for obj in iter:
        yield self._get_subclasses(obj)[0]
    else:
      for obj in iter:
        yield obj
