
from django.urls import path
from . import views

app_name = "estoque"

urlpatterns = [
    path("movimentacao/nova/", views.nova_movimentacao, name="nova_movimentacao"),
    path("historico/", views.historico, name="historico"),
    path("projecao/", views.projecao, name="projecao"),

    # Gerenciamento de produtos
    path("produtos/", views.gerenciar_produtos, name="gerenciar_produtos"),
    path("produtos/novo/", views.novo_produto, name="novo_produto"),
    path("produtos/<int:produto_id>/editar/", views.editar_produto, name="editar_produto"),
    path("produtos/<int:produto_id>/status/", views.alterar_status_produto, name="alterar_status_produto"),

    # Gerenciamento de categorias
    path("categorias/", views.gerenciar_categorias, name="gerenciar_categorias"),
    path("categorias/nova/", views.nova_categoria, name="nova_categoria"),
    path("categorias/<int:categoria_id>/editar/", views.editar_categoria, name="editar_categoria"),
    path("categorias/<int:categoria_id>/excluir/", views.excluir_categoria, name="excluir_categoria"),
]
