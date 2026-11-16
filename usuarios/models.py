from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    class TipoUsuario(models.TextChoices):
        ADM = 'ADM', 'Administrador'
        FUNCIONARIO = 'FUNCIONARIO', 'Funcionário'

    tipo = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.FUNCIONARIO
    )

    autorizado = models.BooleanField(default=False)

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    escola = models.CharField(
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.username