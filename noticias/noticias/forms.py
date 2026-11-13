from django.forms import ModelForm
from django import forms
from .models import Noticia, Categoria


class NoticiaForm(ModelForm):
    class Meta:
        model = Noticia # modelo relacionado a este formulário.
        fields = "__all__" # Puxa todos os campos do modelo automaticamente.

        # Pesonalização dos campos separadamente:
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form-control w-75 m-auto",
                "placeholder": "Digite o título da notícia",
            }),

            "categoria": forms.Select(attrs={
                "class": "form-select w-75 m-auto",
            }),

            "imagem": forms.ClearableFileInput(attrs={
                "class": "form-control w-75 m-auto",
            }),

            "data": forms.DateInput(attrs={
                "class": "form-control w-75 m-auto",
                "type": "date",
                "placeholder": "Digite a data da notícia",
            }),

            "fonte": forms.TextInput(attrs={
                "class": "form-control w-75 m-auto",
                "placeholder": "Informe a fonte da notícia",
            }),

            "texto": forms.Textarea(attrs={
                "class": "form-control w-75 m-auto",
                "placeholder": "Digite o conteúdo da notícia",
                "rows": 8,
            }),

            "publicada": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria # Modelo associado
        fields = ["nome"] # Colunas do banco para a criação dos campos

        # Personalização do campo
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Digite o nome da categoria",
            }),
        }

    # Impede nomes repetidos que só diferem em maiúsculas/minúsculas:
    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()

        repetidas = Categoria.objects.filter(nome__iexact=nome)
        if self.instance.pk:
            repetidas = repetidas.exclude(pk=self.instance.pk) # ao editar, ignora ela mesma.

        if repetidas.exists():
            raise forms.ValidationError("Já existe uma categoria com este nome.")

        return nome
