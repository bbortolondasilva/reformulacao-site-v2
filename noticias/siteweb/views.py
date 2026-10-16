from django.shortcuts import render
from django.http import Http404

PAGINAS = {
    "Remoto-SoftControl.zip": "assets/download/Remoto-SoftControl.zip", 
    "anydesk-5-5-3.exe": "assets/download/anydesk-5-5-3.exe",
}

def home(request):
    return render(request, "siteweb/index.html")

def produtos(request):
    return render(request, "siteweb/produtos.html")

def sobre(request):
    return render(request, "siteweb/sobre.html")

def contato(request):
    return render(request, "siteweb/contato.html")

def atuacao(request):
    return render(request, "siteweb/atuacao.html")

def downloads(request):
    return render(request, "siteweb/downloads.html")

def downloads_obrigado(request):
    arquivo = request.GET.get("arquivo", "")
    caminho = PAGINAS.get(arquivo)

    if not caminho:
        raise Http404("Arquivo de download não encontrado")
    else:    
        return render(request, "siteweb/obrigado.html", {"arquivo": arquivo, "caminho_download": caminho})
