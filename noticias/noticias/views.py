from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max, Min
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.views.decorators.http import require_POST
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

    # Verifica se existe uma próxima notícia:
    proxima = Noticia.objects.filter(id__gt=idNoticia).exists()
    # Verifica se existe uma notícia anterior:
    anterior = Noticia.objects.filter(id__lt=idNoticia).exists()

    return render(request, "noticias/noticia-full.html", {
        "noticia": noticia,
        # Envia os testes de próxima e anterior para a interface para poder controlar a existência dos botões nela.
        "proxima": proxima,
        "anterior": anterior,
    })

# Próxima notícia:
def proximaNoticia(request, idNoticia):
    noticia = get_object_or_404(Noticia, pk=idNoticia)

    # Próximo id no banco de dados:
    proxima = Noticia.objects.filter(
        id__gt = idNoticia # filtra as noticias com id maior que o idNoticia passado.
    ).order_by("id").first() # ordena de forma crescente e pega o primeiro id da lista.

    # Se tiver uma próxima notícia:
    if proxima:
        return redirect("noticias:noticia-full", idNoticia=proxima.id) # redireciona para a noticia full com dados da próxima notícia.

    return redirect("noticias:noticia-full", idNoticia=noticia.id) # redireciona para a noticia atual.

# Notícia anterior:
def noticiaAnterior(request, idNoticia):
    noticia = get_object_or_404(Noticia, pk=idNoticia)

    # Id anterior no banco de dados:
    anterior = Noticia.objects.filter(
        id__lt = idNoticia # Filtra as noticias com id menor que o idNoticia passado.
    ).order_by("-id").first() # Ordena de forma decrescente e pega o primeiro id da lista.

    # Se tiver uma notícia anterior:
    if anterior:
        return redirect("noticias:noticia-full", idNoticia=anterior.id) # Redireicona para a notícia-full com dados da notícia anterior.

    return redirect("noticias:noticia-full", idNoticia=idNoticia) # Redireciona paraa noticia atual.


# CREATE:
# Criar uma nova notícia:
@permission_required("noticias.add_noticia") # precisa de permissão para poder executar.

def criarNoticia(request):
    # Se dados forem enviados no formulário:
    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES) # request.POST recebe os dados textuais do formulário, request.FILES recebe a imagem enviada no formulário.

        # Se o formulário for válido:
        if form.is_valid():
            form.save() # Salva no banco
            return redirect("noticias:listar") # redireciona para a listagem de notícias.

    # Se for apenas acesso ao formulário:
    else:
        form = NoticiaForm() # Atribui os campos do formulário vazios.

    return render(request, "noticias/criar-noticia.html", {
        "form": form
    })


#DELETE:
# Excluir uma notícia:
@permission_required("noticias.delete_noticia") # precisa de permissao para executar.

def excluirNoticia(request, idNoticia):
    # Se for enviada uma notícia para exclusã:
    if request.method == "POST":
        noticia = get_object_or_404(Noticia, pk=idNoticia)

        # Exclui a imagem da pasta media
        noticia.imagem.delete(save=False) # save=False garante a exclusão

        # Exclui o registro do banco de dados
        noticia.delete()

        return redirect("noticias:listar") # Redireciona para a listagem de notícias.


# UPDATE: 
# Editar uma notícia:
@permission_required("noticias.change_noticia") # precisa de permissao para executar.

def editarNoticia(request, idNoticia):
    # Notícia selecionada para edição
    noticia = get_object_or_404(Noticia, pk=idNoticia)

    # Se a requisição for post
    if request.method == "POST":
        # Instancia o formulário
        form = NoticiaForm(
            request.POST, # Envia os novos dados textuais
            request.FILES, # Envia a nova imagem
            instance=noticia # Associa ao registro que já existe daquela notícia.
        )

        # Se o formulário for válido:
        if form.is_valid():
            form.save() # Salva os dados no banco
            return redirect("noticias:noticia-full", idNoticia=noticia.pk) # redireciona para a mesma notícia, já com as alterações.

    else:
        form = NoticiaForm(instance=noticia) # Atribui os dados já existentes da notícia. Instance=notica, associa ao registro existente da notícia para puxar os dados.

    return render(request, "noticias/editar-noticia.html", { # Renderiza a página de notícias e envia os dados da notícia e do formulário.
        "noticia": noticia,
        "form": form,
    })


# Mudar a visibilidade de uma noticia:
@permission_required("noticias.change_noticia")

def visibilidadeNoticia(user):
    if user.has_perm("noticias.change_noticia"):
        return Noticia.objects.all()
    return Noticia.objects.filter(publicada=True)
