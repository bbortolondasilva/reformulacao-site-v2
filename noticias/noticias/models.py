from django.db import models

# Create your models here.
class Noticia(models.Model):
    titulo = models.CharField(max_length=120) # Título da notícia
    imagem = models.ImageField(upload_to="noticias/") # Imagem da notícia
    data = models.DateField() # Data da notícia
    fonte = models.CharField(max_length=300) # Fonte de onde a notícia foi tirada
    texto = models.TextField() # Texto da notícia

    def __str__(self):
        return self.titulo
    