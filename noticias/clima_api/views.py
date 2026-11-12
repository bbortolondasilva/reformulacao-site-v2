from django.shortcuts import render

from .services import obter_clima


def inicio(request):
    # Usa o mesmo template da home, que já tem o card de clima
    return render(request, 'base/index.html', obter_clima())
