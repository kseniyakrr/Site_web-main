from django.db.models import Count
from django import template

from homepage.models import Category, TagPost


register = template.Library()

@register.inclusion_tag('homepage/list_category.html') 
def show_categories(cat_selected=0):
    """Отображает список категорий пиццы."""
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('homepage/list_tags.html')
def show_tags():
    tags = TagPost.objects.all()
    return {'tags': tags}
