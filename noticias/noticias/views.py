from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia

# Create your views here.

# READ:

# Listar todas as notícias cadastradas:
def listar(request):
    noticias = Noticia.objects.all()

    return render(request, "noticias/lista-noticias.html", {
        "noticias":noticias
    })

# Trazer dados de uma notícia específica:
def noticiaFull(request, idNoticia):
    noticia = get_object_or_404(Noticia, pk=idNoticia)

    return render(request, "noticias/noticia-full.html", {
        "noticia": noticia,
    })
