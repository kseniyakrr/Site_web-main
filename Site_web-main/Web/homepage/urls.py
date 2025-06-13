from django.urls import converters
from django.urls import path, register_converter
from . import views
from .converters import CurrencyConverter
from .converters import FloatConverter
register_converter(CurrencyConverter, 'currency')
register_converter(FloatConverter, 'float')
from .views import PizzaCategory, addpage


urlpatterns = [
    path('', views.PizzaHome.as_view(), name='homepage'),
    path('pizza/<slug:pizza_slug>/', views.ShowPost.as_view(), name='pizza_detail'),
    path('menu/', views.menu, name='menu'),  
    path('category/<slug:cat_slug>/', views.PizzaCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('about/', views.about, name='about'),
    path('pizza/<slug:slug>/edit/', views.UpdatePage.as_view(), name='edit'),
    path('delete/<int:pk>/', views.DeletePizza.as_view(), name='delete_pizza'),
    path('recipe/', views.recipe, name='recipe'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/delete/<int:pk>/', views.recipe_delete, name='recipe_delete'),
    path('recipe/edit/<int:pk>/', views.recipe_edit, name='recipe_edit'),
    path('pizza/<slug:slug>/like/', views.like_pizza, name='like_pizza'),
    path('pizza/<slug:slug>/dislike/', views.dislike_pizza, name='dislike_pizza'),
    path('add_comment/<slug:slug>/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pizza_id>/', views.add_pizza_to_cart, name='add_pizza'),
    path('cart/remove/<int:pizza_id>/', views.remove_pizza_from_cart, name='remove_pizza'),
    path('cart/checkout/', views.checkout_view, name='checkout'),
]
