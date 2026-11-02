from django.urls import path
from . import views

app_name = "noticias"

urlpatterns = [
    path("", views.listar, name="listar"),
    path("<int:idNoticia>/", views.noticiaFull, name="noticia-full"),
    path("criar-noticia/", views.criarNoticia, name="criar-noticia"),
]