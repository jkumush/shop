from django import template
from appshop.models import Category

register = template.Library()

@register.simple_tag(name='categories')
def categories():    
    return Category.objects.all()

