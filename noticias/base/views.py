from django.shortcuts import render
from django.http import Http404

ARQUIVOS = {
    "Remoto-SoftControl.zip": "assets/download/Remoto-SoftControl.zip", 
    "anydesk-5-5-3.exe": "assets/download/anydesk-5-5-3.exe",
}

def home(request):
    return render(request, "base/index.html")

def produtos(request):
    return render(request, "base/produtos.html")

def sobre(request):
    return render(request, "base/sobre.html")

def contato(request):
    return render(request, "base/contato.html")

def downloads(request):
    return render(request, "base/downloads.html")

def download_obrigado(request):
    arquivo = request.GET.get("arquivo", "")
    caminho = ARQUIVOS.get(arquivo)

    if not caminho:
        raise Http404("Arquivo de download não encontrado")
    
    return render(request, "base/download_obrigado.html", {"arquivo": arquivo, "caminho_download": caminho})
