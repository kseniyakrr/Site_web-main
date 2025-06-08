homepage = [{'title': "Загрузить файл", 'url_name': 'about'},
 {'title': "Добавить пиццу", 'url_name':
'add_page'},
 {'title': "Войти", 'url_name': 'login'}
]
class DataMixin:
    paginate_by = 2
    title_page = None
    extra_context = {}
    
    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        
    def get_mixin_context(self, context, **kwargs):
        context = context or {}
        if self.title_page:
            context['title'] = self.title_page
        context.update(kwargs)
        return context