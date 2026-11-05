from django.urls import path
from . import views

app_name = "noticias"

urlpatterns = [
    path("", views.listar, name="listar"),
    path("<int:idNoticia>/", views.noticiaFull, name="noticia-full"),
    path("<int:idNoticia>/excluir/", views.excluirNoticia, name="excluir-noticia"),
    path("criar-noticia/", views.criarNoticia, name="criar-noticia"),
    path("<int:idNoticia>/editar-noticia/", views.editarNoticia, name="editar-noticia"),
    path("<int:idNoticia>/proxima/", views.proximaNoticia, name="proxima-noticia"),
    path("<int:idNoticia>/anterior/", views.noticiaAnterior, name="noticia-anterior"),
]