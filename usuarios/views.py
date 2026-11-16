
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

from .forms import CadastroUsuarioForm
from .models import Usuario


def cadastro(request):

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Cadastro realizado! Aguarde a autorização do administrador.'
            )

            return redirect('login')

    else:
        form = CadastroUsuarioForm()

    return render(
        request,
        'usuarios/cadastro.html',
        {'form': form}
    )


@login_required
def inicio(request):
    return render(request, 'usuarios/inicio.html')


def eh_administrador(user):
    return (
        user.is_authenticated
        and user.tipo == Usuario.TipoUsuario.ADM
        and user.is_staff
    )


@login_required
@user_passes_test(eh_administrador)
def aprovacoes(request):

    pendentes = Usuario.objects.filter(
        tipo=Usuario.TipoUsuario.FUNCIONARIO,
        autorizado=False,
        is_active=True
    ).order_by('date_joined')

    return render(
        request,
        'usuarios/aprovacoes.html',
        {'pendentes': pendentes}
    )


@require_POST
@login_required
@user_passes_test(eh_administrador)
def aprovar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        id=usuario_id,
        tipo=Usuario.TipoUsuario.FUNCIONARIO
    )

    usuario.autorizado = True
    usuario.save(update_fields=['autorizado'])

    messages.success(
        request,
        f'O funcionário {usuario.username} foi autorizado.'
    )

    return redirect('usuarios:aprovacoes')


@require_POST
@login_required
@user_passes_test(eh_administrador)
def rejeitar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        id=usuario_id,
        tipo=Usuario.TipoUsuario.FUNCIONARIO
    )

    usuario.is_active = False
    usuario.save(update_fields=['is_active'])

    messages.success(
        request,
        f'O cadastro de {usuario.username} foi rejeitado.'
    )

    return redirect('usuarios:aprovacoes')

@login_required
@user_passes_test(eh_administrador)
def administracao(request):
    return render(request, 'usuarios/administracao.html')
