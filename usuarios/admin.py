
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'tipo',
        'autorizado',
        'is_active',
    )

    list_filter = (
        'tipo',
        'autorizado',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Dados do Confiro Já', {
            'fields': (
                'tipo',
                'autorizado',
                'telefone',
                'escola',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados do Confiro Já', {
            'fields': (
                'tipo',
                'autorizado',
                'telefone',
                'escola',
            )
        }),
    )
