from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'confirmation_code', 'password',
                    'is_staff', 'is_active',)
    search_fields = ('email',)
    list_filter = ('email', 'is_staff', 'is_active',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
