
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import Sum


class Categoria(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da categoria"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Produto(models.Model):

    class UnidadeMedida(models.TextChoices):
        UNIDADE = "UN", "Unidade"
        PACOTE = "PCT", "Pacote"
        CAIXA = "CX", "Caixa"
        QUILOGRAMA = "KG", "Quilograma"
        GRAMA = "G", "Grama"
        LITRO = "L", "Litro"
        MILILITRO = "ML", "Mililitro"
        METRO = "M", "Metro"

    nome = models.CharField(
        max_length=150,
        verbose_name="Nome do produto"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="produtos",
        verbose_name="Categoria"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    unidade = models.CharField(
        max_length=10,
        choices=UnidadeMedida.choices,
        default=UnidadeMedida.UNIDADE,
        verbose_name="Unidade de medida"
    )
    estoque_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Estoque mínimo"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Produto ativo"
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    @property
    def saldo_atual(self):
        entradas = Movimentacao.objects.filter(
            produto=self,
            tipo="ENTRADA"
        ).aggregate(
            total=Sum("quantidade")
        )["total"] or Decimal("0")

        saidas = Movimentacao.objects.filter(
            produto=self,
            tipo="SAIDA"
        ).aggregate(
            total=Sum("quantidade")
        )["total"] or Decimal("0")

        return entradas - saidas

    def __str__(self):
        return self.nome


class Movimentacao(models.Model):

    class TipoMovimentacao(models.TextChoices):
        ENTRADA = "ENTRADA", "Entrada"
        SAIDA = "SAIDA", "Saída"

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="movimentacoes"
    )
    tipo = models.CharField(
        max_length=10,
        choices=TipoMovimentacao.choices
    )
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="movimentacoes"
    )
    observacao = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ["-criada_em"]

    def clean(self):
        super().clean()

        if not self.produto_id or not self.tipo or not self.quantidade:
            return

        if self.tipo == self.TipoMovimentacao.SAIDA:
            movimentos = Movimentacao.objects.filter(
                produto_id=self.produto_id
            ).exclude(pk=self.pk)

            entradas = movimentos.filter(
                tipo="ENTRADA"
            ).aggregate(
                total=Sum("quantidade")
            )["total"] or Decimal("0")

            saidas = movimentos.filter(
                tipo="SAIDA"
            ).aggregate(
                total=Sum("quantidade")
            )["total"] or Decimal("0")

            saldo = entradas - saidas

            if self.quantidade > saldo:
                raise ValidationError({
                    "quantidade": (
                        f"Saldo insuficiente. Disponível: {saldo}."
                    )
                })

    def save(self, *args, **kwargs):
        with transaction.atomic():
            produto = Produto.objects.select_for_update().get(
                pk=self.produto_id
            )
            self.produto = produto

            self.full_clean()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome}"
