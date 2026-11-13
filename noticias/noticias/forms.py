from django.forms import ModelForm
from django import forms
from .models import Noticia


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
