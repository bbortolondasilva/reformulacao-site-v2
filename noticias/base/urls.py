from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("produtos/", views.produtos, name="produtos"),
    path("downloads/", views.downloads, name="downloads"),
    path("download_obrigado/", views.download_obrigado, name="download_obrigado"),
    path("sobre/", views.sobre, name="sobre"),
    path("contato/", views.contato, name="contato"),
]