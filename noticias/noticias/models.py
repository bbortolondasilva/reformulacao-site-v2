from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=60, unique=True) # Nome da categoria

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

class Noticia(models.Model):
    titulo = models.CharField(max_length=120) # Título da notícia

    # Categoria da notícia.
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT, # Se houver uma notícia dentro da categoria, ela não pode ser excluída.
        null=True,
        blank=True,
        related_name="noticias",
    )

    imagem = models.ImageField(upload_to="noticias/") # Imagem da notícia
    data = models.DateField() # Data da notícia
    fonte = models.CharField(max_length=300) # Fonte de onde a notícia foi tirada
    texto = models.TextField() # Texto da notícia
    publicada = models.BooleanField(
        default=False, 
        verbose_name="Publicada",
        help_text="Marque para que a notícia fique visível para o público."
    ) # Visibilidade da notícia 

    def __str__(self):
        return self.titulo
    