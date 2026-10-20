from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia
from .forms import NoticiaForm

# Create your views here.
def listar(request):
    noticias = Noticia.objects.all()

    return render(request, "noticias/noticias.html", {
        "noticias":noticias
    })
