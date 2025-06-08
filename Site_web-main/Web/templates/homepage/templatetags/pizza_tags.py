from django import template
from Web.homepage.views import categories_db 

register = template.Library()

@register.inclusion_tag('homepage/list_categories.html') 
def show_categories(cat_selected=0):
    """Отображает список категорий пиццы."""
    cats = categories_db  
    return {'cats': cats, 'cat_selected': cat_selected}