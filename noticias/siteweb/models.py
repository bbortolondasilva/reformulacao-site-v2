from django.db import models

# Create your models here.
class Noticia(models.Model):
    titulo = models.CharField(max_length=120)
    imagem = models.ImageField()
    data = models.DateField()
    fonte = models.CharField(max_length=300)
    texto = models.CharField()

    def __str__(self):
        return self.titulo
