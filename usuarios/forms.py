from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario


class CadastroUsuarioForm(UserCreationForm):

    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=20, required=False)
    escola = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Usuario
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'telefone',
            'escola',
        )

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.tipo = Usuario.TipoUsuario.FUNCIONARIO
        usuario.autorizado = False

        if commit:
            usuario.save()

        return usuario


class LoginUsuarioForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if not user.autorizado:
            raise ValidationError(
                'Seu cadastro ainda aguarda autorização do administrador.',
                code='nao_autorizado'
            )