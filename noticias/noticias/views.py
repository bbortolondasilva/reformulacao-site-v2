from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia
from .forms import NoticiaForm

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

# Criar uma nova notícia:
def criarNoticia(request):
    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES) # request.POST recebe os dados textuais do formulário, request.FILES recebe a imagem enviada no formulário.

        if form.is_valid():
            form.save()
            return redirect("noticias:listar")

    else:
        form = NoticiaForm()

    return render(request, "noticias/criar-noticia.html", {
        "form": form
    })

# Excluir uma notícia:
def excluirNoticia(request, idNoticia):
    if request.method == "POST":
        noticia = get_object_or_404(Noticia, pk=idNoticia)
        noticia.delete()

        return redirect("noticia:listar")
