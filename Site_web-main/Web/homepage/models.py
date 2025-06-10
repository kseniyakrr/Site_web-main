import itertools
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
User = settings.AUTH_USER_MODEL

class AvailablePizzaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=Pizza.Status.AVAILABLE)

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name = 'Категория')
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})
      
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)  # Определяем base_slug перед использованием
            unique_slug = base_slug
            num = 1
            while Category.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д':
'd',
 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и':
'i', 'к': 'k',
 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п':
'p', 'р': 'r',
 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х':
'h', 'ц': 'c', 'ч': 'ch',
 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y',
'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class Pizza(models.Model):
    class Status(models.IntegerChoices):
        NOTAVAILABLE = 0, 'Нет в наличии'
        AVAILABLE = 1, 'Есть в наличии'
    name = models.CharField(max_length=255, verbose_name = 'Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    diameter = models.PositiveIntegerField(default = 30,verbose_name='Диаметр (см)')
    is_available = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.NOTAVAILABLE, verbose_name="Статус")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    image = models.ImageField(upload_to="pizzas/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default = 1, verbose_name = 'Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='pizzas', verbose_name = 'Тэги')
    history = models.OneToOneField('PizzaHistory', on_delete=models.SET_NULL, null=True, related_name='history', verbose_name = 'История создания')
    history_text = models.TextField(blank=True, verbose_name='История создания')  # Новое текстовое поле
    likes = models.ManyToManyField(User, related_name='liked_pizzas', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_pizzas', blank=True)


    
    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'


        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = orig = slugify(self.name)
            
            # Проверка уникальности и добавление суффикса при необходимости
            for x in itertools.count(1):
                if not Pizza.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{orig}-{x}'
                
        super().save(*args, **kwargs)


    objects = models.Manager()
    published = AvailablePizzaManager()

    def get_absolute_url(self):
        return reverse('pizza_detail', kwargs={'pizza_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'
        ordering = ['name']

    
    


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
    def __str__(self):
        return self.tag

class PizzaHistory(models.Model):
    name = ''
    inspiration = models.TextField(blank=True)
    def __str__(self):
        return self.name

       
class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    class Meta:
        verbose_name = "Загруженный файл"
        verbose_name_plural = "Загруженные файлы"

    def __str__(self):
        return f"Файл {self.file.name} от {self.uploaded_at}"


class Recipe(models.Model):
    title = models.CharField("Название", max_length=200)
    ingredients = models.TextField("Ингредиенты")
    instructions = models.TextField("Инструкция")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    image = models.ImageField("Фото", upload_to='recipes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def user_can_delete(self, user):
        return user == self.author or user.is_superuser
    
class Comment(models.Model):
    pizza = models.ForeignKey('Pizza', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Используем AUTH_USER_MODEL
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author.username}'
    