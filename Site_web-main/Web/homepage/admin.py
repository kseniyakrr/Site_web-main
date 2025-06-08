from pyexpat.errors import messages
from django.contrib import admin
from .models import Category, Pizza
from django.utils.safestring import mark_safe
from .models import Recipe
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
admin.site.register(User, UserAdmin)


admin.site.register(Recipe)

class HistoryFilter(admin.SimpleListFilter):
    title = 'История создания'
    parameter_name = 'history_of_created'
    
    def lookups(self, request, model_admin):
        return [
            ('yes_history', 'Есть история создания'),
            ('no_history', 'Нет истории создания'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'yes_history':
            return queryset.filter(history_text__isnull=False)
        elif self.value() == 'no_history':
            return queryset.filter(history_text__isnull=True)
        return queryset



@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'description', 'category', 'price', 'diameter', 'history_text', 'tags', 'image']
    filter_horizontal = ['tags']
    # readonly_fields = ['slug']
    prepopulated_fields = {"slug": ("name", )}
    list_display = ('id', 'name', 'time_create','is_available', 'post_photo', 'price', 'is_expensive')
    list_display_links = ('name', )
    list_editable = ('is_available', 'price', )
    ordering = ['-time_create', 'name']
    list_per_page = 5
    actions = ['set_available', 'set_draft']
    search_fields = ['name', 'category__name']
    list_filter = [HistoryFilter, 'category__name', 'is_available']


    @admin.display(description="Изображение")
    def post_photo(self, pizza: Pizza):
        if pizza.image:
            return mark_safe(f"<img src='{pizza.image.url}' width=50>")
        return "Без фото"
    
    @admin.display(description = 'Дорогие пиццы')
    def is_expensive(self, obj):
        return obj.price > 650
    is_expensive.boolean = True

    

    @admin.action(description="Сделать пиццы доступными")
    def set_available(self, request, queryset): 
        count = queryset.update(is_available=Pizza.Status.AVAILABLE)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_available=Pizza.Status.NOTAVAILABLE)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!")

    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
