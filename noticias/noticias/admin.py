from django.contrib import admin
from .models import Noticia, Categoria

# Register your models here.
admin.site.register(Noticia)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nome",)
