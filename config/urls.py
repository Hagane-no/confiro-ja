from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios.forms import LoginUsuarioForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("usuarios.urls")),
    path("estoque/", include("estoque.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="usuarios/login.html",
            authentication_form=LoginUsuarioForm
        ),
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout"
    ),
]
