
from datetime import timedelta
from decimal import Decimal, ROUND_CEILING

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import MovimentacaoForm, ProdutoForm, CategoriaForm
from .models import Movimentacao, Produto, Categoria


def usuario_adm(user):
    return (
        user.is_authenticated
        and getattr(user, "tipo", None) == "ADM"
        and user.is_staff
    )


adm_required = user_passes_test(usuario_adm)


@login_required
def nova_movimentacao(request):
    if request.method == "POST":
        form = MovimentacaoForm(request.POST)

        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.responsavel = request.user
            movimentacao.save()

            messages.success(
                request,
                "Movimentação registrada com sucesso!"
            )

            return redirect("estoque:historico")
    else:
        form = MovimentacaoForm()

    return render(request, "estoque/movimentacao_form.html", {
        "form": form
    })


@login_required
def historico(request):
    movimentacoes = Movimentacao.objects.select_related(
        "produto", "responsavel"
    ).order_by("-criada_em")

    return render(request, "estoque/historico.html", {
        "movimentacoes": movimentacoes
    })


@login_required
def projecao(request):
    hoje = timezone.localdate()
    inicio_periodo = timezone.now() - timedelta(days=30)

    produtos = Produto.objects.filter(
        ativo=True
    ).select_related("categoria").order_by("nome")

    resultados = []

    for produto in produtos:
        saldo = produto.saldo_atual

        consumo = Movimentacao.objects.filter(
            produto=produto,
            tipo="SAIDA",
            criada_em__gte=inicio_periodo
        ).aggregate(
            total=Sum("quantidade")
        )["total"] or Decimal("0")

        media_diaria = consumo / Decimal("30")

        dias_restantes = None
        data_esgotamento = None

        if saldo <= 0:
            situacao = "Esgotado"
        elif saldo <= produto.estoque_minimo:
            situacao = "Estoque baixo"
        else:
            situacao = "Estoque adequado"

        if media_diaria > 0 and saldo > 0:
            dias_restantes = int(
                (saldo / media_diaria).to_integral_value(
                    rounding=ROUND_CEILING
                )
            )

            data_esgotamento = hoje + timedelta(
                days=dias_restantes
            )

        resultados.append({
            "produto": produto,
            "saldo": saldo,
            "consumo": consumo,
            "media_diaria": media_diaria,
            "dias_restantes": dias_restantes,
            "data_esgotamento": data_esgotamento,
            "situacao": situacao,
        })

    return render(request, "estoque/projecao.html", {
        "resultados": resultados,
        "data_referencia": hoje,
    })


@login_required
@adm_required
def gerenciar_produtos(request):
    produtos = Produto.objects.select_related(
        "categoria"
    ).order_by("nome")

    return render(request, "estoque/gerenciar_produtos.html", {
        "produtos": produtos
    })


@login_required
@adm_required
def novo_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect("estoque:gerenciar_produtos")
    else:
        form = ProdutoForm()

    return render(request, "estoque/produto_form.html", {
        "form": form,
        "titulo": "Cadastrar produto",
    })


@login_required
@adm_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)

        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("estoque:gerenciar_produtos")
    else:
        form = ProdutoForm(instance=produto)

    return render(request, "estoque/produto_form.html", {
        "form": form,
        "titulo": "Editar produto",
        "produto": produto,
    })


@login_required
@adm_required
@require_POST
def alterar_status_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    produto.ativo = not produto.ativo
    produto.save()

    if produto.ativo:
        messages.success(request, "Produto reativado com sucesso!")
    else:
        messages.success(request, "Produto desativado com sucesso!")

    return redirect("estoque:gerenciar_produtos")


@login_required
@adm_required
def gerenciar_categorias(request):
    categorias = Categoria.objects.all().order_by("nome")

    return render(request, "estoque/gerenciar_categorias.html", {
        "categorias": categorias
    })


@login_required
@adm_required
def nova_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Categoria cadastrada com sucesso!")
            return redirect("estoque:gerenciar_categorias")
    else:
        form = CategoriaForm()

    return render(request, "estoque/categoria_form.html", {
        "form": form,
        "titulo": "Cadastrar categoria",
    })


@login_required
@adm_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)

        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso!")
            return redirect("estoque:gerenciar_categorias")
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, "estoque/categoria_form.html", {
        "form": form,
        "titulo": "Editar categoria",
        "categoria": categoria,
    })


@login_required
@adm_required
@require_POST
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)

    try:
        categoria.delete()
        messages.success(request, "Categoria excluída com sucesso!")
    except ProtectedError:
        messages.error(
            request,
            "Não é possível excluir esta categoria: existem produtos vinculados."
        )

    return redirect("estoque:gerenciar_categorias")
