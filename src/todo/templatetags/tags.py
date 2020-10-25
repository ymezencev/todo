from django.template import Library
from django.core import serializers


register = Library()

@register.filter
def json(queryset):
    return serializers.serialize('json', queryset)
