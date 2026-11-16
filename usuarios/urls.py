
from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),

    path('', views.inicio, name='inicio'),

    path('aprovacoes/', views.aprovacoes, name='aprovacoes'),

    path(
        'aprovar/<int:usuario_id>/',
        views.aprovar_usuario,
        name='aprovar_usuario'
    ),

    path(
        'rejeitar/<int:usuario_id>/',
        views.rejeitar_usuario,
        name='rejeitar_usuario'
    ),

    path(
        'administracao/',
        views.administracao,
        name='administracao'
    ),
]
