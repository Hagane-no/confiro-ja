
from django.contrib import admin
from .models import Categoria, Produto, Movimentacao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "criada_em")
    search_fields = ("nome", "descricao")


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "categoria",
        "unidade",
        "estoque_minimo",
        "ativo",
        "exibir_saldo",
    )

    list_filter = ("categoria", "unidade", "ativo")
    search_fields = ("nome", "descricao")
    list_editable = ("estoque_minimo", "ativo")

    @admin.display(description="Saldo atual")
    def exibir_saldo(self, obj):
        return obj.saldo_atual


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = (
        "produto",
        "tipo",
        "quantidade",
        "responsavel",
        "criada_em",
    )

    list_filter = ("tipo", "criada_em", "produto")
    search_fields = ("produto__nome", "responsavel__username")
    readonly_fields = ("responsavel", "criada_em")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.responsavel = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False
