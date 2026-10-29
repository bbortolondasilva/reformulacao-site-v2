from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia

# Create your views here.
def listar(request):
    noticias = Noticia.objects.all()

    return render(request, "noticias/lista-noticias.html", {
        "noticias":noticias
    })
