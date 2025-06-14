# Generated by Django 4.2.20 on 2025-06-08 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0026_remove_pizza_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('ingredients', models.TextField(verbose_name='Ингредиенты')),
                ('instructions', models.TextField(verbose_name='Инструкция')),
                ('author_name', models.CharField(blank=True, max_length=100, verbose_name='Автор')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='Фото')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
