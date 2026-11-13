from datetime import date

from rest_framework import serializers

from .models import Noticia

# Limites usados nas validações
TAMANHO_MAX_IMAGEM_MB = 5
TITULO_MIN = 5
TEXTO_MIN = 20


class NoticiaSerializer(serializers.ModelSerializer):
    """Converte a Notícia em JSON (e vice-versa) e valida os dados recebidos pela API."""

    class Meta:
        model = Noticia
        fields = ["id", "titulo", "imagem", "data", "fonte", "texto"]
        read_only_fields = ["id"]
        # Mensagens próprias para campos obrigatórios
        extra_kwargs = {
            "titulo": {"error_messages": {"required": "Informe o título da notícia.",
                                          "blank": "Informe o título da notícia."}},
            "imagem": {"error_messages": {"required": "Envie uma imagem para a notícia.",
                                          "empty": "Envie uma imagem para a notícia.",
                                          "invalid_image": "O arquivo enviado não é uma imagem válida."}},
            "data": {"error_messages": {"required": "Informe a data da notícia.",
                                        "invalid": "Data inválida. Use o formato AAAA-MM-DD."}},
            "fonte": {"error_messages": {"required": "Informe a fonte da notícia.",
                                         "blank": "Informe a fonte da notícia."}},
            "texto": {"error_messages": {"required": "Informe o texto da notícia.",
                                         "blank": "Informe o texto da notícia."}},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Na edição (PUT/PATCH) a imagem é opcional: se não enviar, mantém a atual.
        if self.instance is not None and "imagem" in self.fields:
            self.fields["imagem"].required = False

    # ---------- Validações de cada campo ----------

    def validate_titulo(self, valor):
        valor = valor.strip()
        if len(valor) < TITULO_MIN:
            raise serializers.ValidationError(
                f"O título deve ter pelo menos {TITULO_MIN} caracteres."
            )
        return valor

    def validate_data(self, valor):
        if valor > date.today():
            raise serializers.ValidationError("A data da notícia não pode ser no futuro.")
        return valor

    def validate_fonte(self, valor):
        valor = valor.strip()
        if not valor:
            raise serializers.ValidationError("Informe a fonte da notícia.")
        return valor

    def validate_texto(self, valor):
        valor = valor.strip()
        if len(valor) < TEXTO_MIN:
            raise serializers.ValidationError(
                f"O texto deve ter pelo menos {TEXTO_MIN} caracteres."
            )
        return valor

    def validate_imagem(self, valor):
        if valor and valor.size > TAMANHO_MAX_IMAGEM_MB * 1024 * 1024:
            raise serializers.ValidationError(
                f"A imagem deve ter no máximo {TAMANHO_MAX_IMAGEM_MB} MB."
            )
        return valor

    # ---------- Validação envolvendo mais de um campo ----------

    def validate(self, dados):
        titulo = dados.get("titulo", getattr(self.instance, "titulo", None))
        data_noticia = dados.get("data", getattr(self.instance, "data", None))

        # Não permite duas notícias com o mesmo título na mesma data
        repetidas = Noticia.objects.filter(titulo__iexact=titulo, data=data_noticia)
        if self.instance is not None:
            repetidas = repetidas.exclude(pk=self.instance.pk)
        if repetidas.exists():
            raise serializers.ValidationError(
                "Já existe uma notícia com este título nesta data."
            )
        return dados
