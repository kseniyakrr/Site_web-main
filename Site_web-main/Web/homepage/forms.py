from django import forms
from .models import Category, Pizza
from django.core.validators import MinLengthValidator
from .models import Recipe
from .models import Comment
""" class PizzaForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label='Название пиццы',
        validators=[MinLengthValidator(3, message="Название должно быть не короче 3 символов")],
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    
    slug = forms.SlugField(
        max_length=255,
        label='URL-адрес',
        validators=[MinLengthValidator(3, message="URL должен быть не короче 3 символов")]
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        required=False,
        label='Описание',
        validators=[MinLengthValidator(10, message="Описание должно быть не короче 10 символов")],

    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Цена',
        min_value=0
    )
    
    diameter = forms.IntegerField(
        label='Диаметр (см)',
        min_value=10,
        max_value=100
    )
    
    is_available = forms.BooleanField(
        required=False,
        label='Доступна для заказа',
        initial=True
    )
    
    image = forms.ImageField(
        required=False,
        label='Изображение пиццы'
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Категория не выбрана'
    )
    
    history_text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}),
        required=False,
        label='История создания'
    )
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        # Разрешенные символы: латинские буквы, цифры, дефисы и подчеркивания
        if not re.match(r'^[a-zA-Z0-9_-]+$', slug):
            raise forms.ValidationError(
                "Slug должен содержать только латинские буквы, цифры, дефисы и подчеркивания."
            )
        return slug
 """

class PizzaForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
             raise forms.ValidationError('Длина превышает 50 символов')
        return name
        
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    image = forms.ImageField(
        label='Фото пиццы',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    
    class Meta:
        model = Pizza
        fields = ['name', 'slug', 'description', 'price', 'diameter', 
                  'is_available', 'image', 'category', 'tags', 'history_text']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'minlength': '3',
                'maxlength': '255'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'minlength': '10'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'size': 4}),
            'history_text': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
            

        }
        
        labels = {
            'name': 'Название пиццы',
            'slug': 'Слаг',
            'description': 'Описание',
            'price': 'Цена',
            'diameter': 'Диаметр (см)',
            'is_available': 'Статус доступности',
            'image': 'Фото',
            'category': 'Категория',
            'tags': 'Тэги',
            'history_text': 'История создания', 
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'author_name', 'image']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 5}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'comment-textarea',
                'placeholder': 'Оставьте ваш комментарий...',
                'rows': 3
            }),
        }