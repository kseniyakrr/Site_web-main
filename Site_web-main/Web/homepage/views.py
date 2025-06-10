
from django.contrib import messages
from unicodedata import category
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from homepage.utils import DataMixin
from .models import Pizza, Category, TagPost, UploadFiles
from django.shortcuts import redirect
from .forms import PizzaForm, UploadFileForm
import os
os.makedirs('uploads', exist_ok=True)
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin  # Добавьте этот импорт
from .forms import RecipeForm
from .models import Recipe
from django.views.decorators.http import require_POST
from .models import Comment
from .forms import CommentForm
from django.utils import timezone
     
def homepage(request):
    # Получаем все пиццы с оптимизацией запросов
    
    pizzas = Pizza.objects.filter(is_available=True).select_related("category")
    
    context = {
        'title': 'Главная страница',
        'pizzas': pizzas,
        'categories': Category.objects.all(),
        'pizzas': Pizza.objects.all(),
        'cat_selected': 0,  # Не используем фильтрацию на сервере
    }
    return render(request, 'homepage/homepage/homepage.html', context)

""" class PizzaHome(TemplateView):
    template_name = 'homepage/homepage/homepage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем ID категории из GET-параметра
        cat_selected = int(self.request.GET.get('cat_id', 0))
        
        # Фильтрация пицц по категории
        if cat_selected:
            pizzas = Pizza.published.filter(category_id=cat_selected).select_related('category')
        else:
            pizzas = Pizza.published.all().select_related('category')
        
        context.update({
            'title': 'Меню пиццерии',
            'pizzas': pizzas,
            'categories': Category.objects.all(),
            'cat_selected': cat_selected,
        })
        
        return context """



class PizzaHome(DataMixin, ListView):
    model = Pizza
    template_name = 'homepage/homepage/homepage.html'
    context_object_name = 'pizzas'
    
    def get_queryset(self):
        queryset = Pizza.published.all().select_related('category')
        
        # Фильтрация по категории, если slug передан в URL
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Добавляем все категории для меню
        context['categories'] = Category.objects.all()
        
        # Определяем выбранную категорию
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = self.category
            context['cat_selected'] = self.category.id
            context['title'] = f'Категория: {self.category.name}'
        else:
            context['cat_selected'] = None
            context['title'] = 'Все пиццы'
            
        # Используем метод mixin для добавления дополнительного контекста
        return self.get_mixin_context(context)




def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')

def exchange(request, pair, amount):
    """Пример простого конвертера валют"""
    rates = {
        # Прямые курсы
        'USD-RUB': 90.50,
        'EUR-USD': 1.07,
        'EUR-RUB': 96.80,
        
        # Обратные курсы (1 / прямой курс)
        'RUB-USD': round(1 / 90.50),
        'USD-EUR': round(1 / 1.07),
        'RUB-EUR': round(1 / 96.80),
        
        # Само-конвертации (курс 1:1)
        'USD-USD': 1.0,
        'EUR-EUR': 1.0,
        'RUB-RUB': 1.0

    }
    try:
        # Обработка входных данных
       
        if amount <= 0:
            raise ValueError
        pair_upper = pair.upper()
        if pair_upper not in rates:
            raise KeyError
            
        # Вычисление результата
        converted = round(amount * rates[pair_upper], 2)
        from_cur = pair_upper[:3]
        to_cur = pair_upper[4:]
        rate = rates[pair_upper]
        
        # Форматирование заголовка
        result_html = f"""
           <h1>Результат конвертации</h1>
           <p><strong>Дата:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
           <p><strong>Сумма:</strong> {amount} {from_cur}</p>
           <p><strong>Курс:</strong> 1 {from_cur} = {rate} {to_cur}</p>
           <h2>Итого: {converted} {to_cur}</h2>
           """
        return HttpResponse(result_html)

    except ValueError:
        return HttpResponse("ОШИБКА: Некорректная сумма", status=400)
    except KeyError:
        return HttpResponse("ОШИБКА: Неподдерживаемая валютная пара", status=400)
    



def menu(request, category_id=0):
    """Отображение пицц по выбранной категории."""
    pizzas = [pizza for pizza in pizzas_db if pizza['category_id'] == category_id or category_id == 0] # List comprehension.

    context = {
        'headline': 'Наше меню',
        'description': 'Выбирайте пиццу на свой вкус!',
        'cta': 'Подробнее',
        'image_url': '/static/images/menu.jpg',
        'title': 'Категории пицц',
        'pizzas': pizzas,
        'categories': categories_db,
        'cat_selected': category_id,
    }
    return render(request, 'menu/menu.html', context)


# def category_list(request, category_slug):
    """Отображает все пиццы в выбранной категории"""
    category = get_object_or_404(Category, slug=category_slug)
    
    # Получаем доступные пиццы этой категории
    pizzas = Pizza.available.filter(category__slug=category_slug)

    context = {
        'category': category,
        'pizzas': Pizza.objects.all(),
        'categories': Category.objects.all(),
        'title': f'Пиццы категории {category.name}',
        'cat_selected': category.slug  # Передаем slug категории
    }

    return render(request, 'homepage/category_list.html', context)

class PizzaCategory(DataMixin, ListView):
    
    context_object_name = 'pizzas'
    allow_empty = False  # Будет 404 если категория пуста или не существует

    def get_queryset(self):
        # Получаем категорию или 404
        self.category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Pizza.published.filter(
            category=self.category
        ).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        return self.get_mixin_context(context, title='Категория - ' + category.name, cat_selected=category.id, )



def pizza_detail(request, pizza_slug):
    pizza = get_object_or_404(Pizza, slug=pizza_slug)
    return render(request, 'pizza_detail/pizza_detail.html', {'pizza': pizza})



class ShowPost(DataMixin, DetailView):
    model = Pizza
    template_name = 'pizza_detail/pizza_detail.html'
    context_object_name = 'pizza'  # Имя переменной в шаблоне
    slug_url_kwarg = 'pizza_slug'  # Параметр из URL

    def get_object(self, queryset=None):
        # Фильтрация только опубликованных пицц
        return get_object_or_404(
            Pizza.published,  # Используем кастомный менеджер
            slug=self.kwargs[self.slug_url_kwarg]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
        title=context['pizza'])



def current_time(request):
    return {
        'current_time': datetime.now()
    }
     

def show_tag(request, tag_slug=None):
    tag = None
    pizzas = Pizza.objects.all()
    
    if tag_slug:
        tag = get_object_or_404(TagPost, slug=tag_slug)
        pizzas = pizzas.filter(tags__in=[tag])
    
    return render(request, 'homepage/homepage.html', {
        'pizzas': pizzas,
        'tag': tag
    })

class TagPostList(DataMixin, ListView):
    template_name = 'homepage/homepage.html'
    context_object_name = 'pizzas'
    allow_empty = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
        title='Тег: ' + tag.tag)
    
    def get_queryset(self):
        return Pizza.published.filter(tags__slug=self.kwargs['tag_slug ']).select_related('category')



def addpage(request):
        if request.method == 'POST':
            form = PizzaForm(request.POST, request.FILES)
            if form.is_valid():
                pizza: Pizza = form.save()
                return redirect('homepage')
            else:
                return render(request, 'homepage/addpage.html', {'form': form})
        else:
            form = PizzaForm()
        return render(request, 'homepage/addpage.html', {'form': form})


""" class AddPage(View):
    def get(self, request):
        form = PizzaForm()
        return render(request, 'homepage/addpage.html', {'form': form})
    def post(self, request):
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        return render(request, 'homepage/addpage.html', {'form': form}) """

""" class AddPage(FormView):
    form_class = PizzaForm
    template_name = 'homepage/addpage.html'
    success_url = reverse_lazy('homepage')
    extra_context = {
        'title': 'Добавление пиццы',
         }
    def form_valid(self, form):
        form.save()
        return super().form_valid(form) """

""" class AddPage(CreateView):
    form_class = PizzaForm
    template_name = 'homepage/addpage.html'
    success_url = reverse_lazy('homepage')
    extra_context = {
         'title': 'Добавление пиццы',
         } """

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    model = Pizza
    fields = ['name', 'slug', 'description', 'is_available', 'category', 'diameter', 'price', 'image', 'tags']
    #form_class = PizzaForm
    template_name = 'homepage/addpage.html'
    success_url = reverse_lazy('homepage')
    title_page = 'Добавление пиццы'
    permission_required = 'homepage.add_pizza'
       
    
class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
     model = Pizza
     fields = ['name', 'description', 'image', 'is_available', 'category']
     template_name = 'homepage/edit.html'
     success_url = reverse_lazy('homepage')
     title_page = 'Редактирование пиццы'
     permission_required = 'homepage.change_pizza'
     
class DeletePizza(DeleteView):
    model = Pizza
    template_name = 'homepage/confirm_delete.html'
    success_url = reverse_lazy('homepage')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление пиццы'
        return context

@login_required
def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Создаем папку для загрузки, если её нет
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Сохраняем файл
                fp = UploadFiles(file=request.FILES['file'])
                fp.save()
                
                messages.success(request, "Файл успешно загружен!")
                return redirect('about')
            except Exception as e:
                messages.error(request, f"Ошибка при загрузке файла: {str(e)}")
        else:
            messages.error(request, "Форма содержит ошибки")
    else:
        form = UploadFileForm()
    
    # Получаем все загруженные файлы для отображения
    files = UploadFiles.objects.all().order_by('-uploaded_at')
    
    return render(request, 'homepage/homepage/about.html', {
        'title': 'О сайте',
        'form': form,
        'files': files
    })

@login_required
def recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm(user=request.user)
    return render(request, 'recipes/recipe.html', {'form': form})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def recipe_list(request):
   
    recipes_queryset = Recipe.objects.all().order_by('-created_at')

    paginator = Paginator(recipes_queryset, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'recipes/recipe_list.html', {'page_obj': page_obj})


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.author or request.user.is_superuser:
        recipe.delete()
        return redirect('recipe_list')
    else:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.user != recipe.author and not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'object': recipe  
    })

@login_required
def like_pizza(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    if request.user in pizza.dislikes.all():
        pizza.dislikes.remove(request.user)
    if request.user in pizza.likes.all():
        pizza.likes.remove(request.user)
        liked = False
    else:
        pizza.likes.add(request.user)
        liked = True
    return JsonResponse({'likes': pizza.likes.count(), 'liked': liked})

@login_required
def dislike_pizza(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    if request.user in pizza.likes.all():
        pizza.likes.remove(request.user)
    if request.user in pizza.dislikes.all():
        pizza.dislikes.remove(request.user)
        disliked = False
    else:
        pizza.dislikes.add(request.user)
        disliked = True
    return JsonResponse({'dislikes': pizza.dislikes.count(), 'disliked': disliked})

@login_required
@require_POST
def add_comment(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    text = request.POST.get('text', '').strip()
    
    if not text:
        return JsonResponse({'success': False, 'error': 'Комментарий не может быть пустым'})
    
    try:
        comment = Comment.objects.create(
            pizza=pizza,
            author=request.user,
            text=text
        )
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'username': request.user.username,
            'text': comment.text,
            'created_at': comment.created_at.strftime("%d.%m.%Y %H:%M")
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Проверка прав
    if not (request.user == comment.author or request.user.is_superuser):
        return JsonResponse({'error': 'Нет прав на удаление'}, status=403)
    
    comment.delete()
    return JsonResponse({'success': True})    



def pizza_list(request):
    category_id = request.GET.get('category')  # Получаем ID категории из параметра URL
    categories = Category.objects.all()
    
    # Фильтруем пиццы по категории или показываем все
    if category_id:
        pizzas = Pizza.objects.filter(category_id=category_id, is_available=True)
        cat_selected = int(category_id)
    else:
        pizzas = Pizza.objects.filter(is_available=True)
        cat_selected = None
    
    context = {
        'pizzas': pizzas,
        'categories': categories,
        'cat_selected': cat_selected,
    }
    return render(request, 'pizza_detail/pizza_list.html', context)


