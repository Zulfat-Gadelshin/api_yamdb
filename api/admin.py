from django.contrib import admin

from .models import Category, CustomUser, Genre, Title


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'confirmation_code', 'password',
                    'is_staff', 'is_active',)
    search_fields = ('email',)
    list_filter = ('email', 'is_staff', 'is_active',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'description', )
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'
