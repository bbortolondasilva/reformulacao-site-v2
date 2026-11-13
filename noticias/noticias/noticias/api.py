from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import filters, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from noticias.models import Noticia
from .serializers import NoticiaSerializer

from noticias.views import noticias_visiveis


@extend_schema_view(
    list=extend_schema(
        summary="Listar notícias",
        description="Retorna as notícias cadastradas, da mais recente para a mais antiga. "
                    "Aberto para qualquer visitante.",
        parameters=[
            OpenApiParameter("search", str, description="Busca no título, fonte e texto."),
            OpenApiParameter("ordering", str, description="Ordenação: data, -data, titulo, -titulo."),
        ],
    ),
    retrieve=extend_schema(
        summary="Consultar uma notícia",
        description="Retorna os dados de uma notícia pelo ID. Aberto para qualquer visitante.",
    ),
    create=extend_schema(
        summary="Criar notícia",
        description="Cadastra uma nova notícia (envio como multipart/form-data por causa da imagem). "
                    "Exige usuário autenticado com a permissão `noticias.add_noticia`.",
    ),
    update=extend_schema(
        summary="Editar notícia (todos os campos)",
        description="Substitui os dados da notícia. A imagem é opcional: se não for enviada, a atual é mantida. "
                    "Exige a permissão `noticias.change_noticia`.",
    ),
    partial_update=extend_schema(
        summary="Editar notícia (campos parciais)",
        description="Altera apenas os campos enviados. Exige a permissão `noticias.change_noticia`.",
    ),
    destroy=extend_schema(
        summary="Excluir notícia",
        description="Exclui a notícia e a imagem dela da pasta media. "
                    "Exige a permissão `noticias.delete_noticia`.",
    ),
)
class NoticiaViewSet(viewsets.ModelViewSet):
    """
    Endpoints de notícias.

    - GET (listar/consultar): liberado para todos.
    - POST, PUT, PATCH, DELETE: só usuários logados com a permissão do Django
    correspondente (add, change, delete) — as mesmas usadas nas telas do site.
    """

    queryset = Noticia.objects.all().order_by("-data", "-id")
    serializer_class = NoticiaSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["titulo", "fonte", "texto"]
    ordering_fields = ["data", "titulo", "id"]

    # Aplica a mesma regra de visibilidade do site: visitante só vê as publicadas.
    def get_queryset(self):
        return noticias_visiveis(self.request.user).order_by("-data", "-id")

    def perform_update(self, serializer):
        imagem_antiga = serializer.instance.imagem
        nova_imagem = serializer.validated_data.get("imagem")
        noticia = serializer.save()

        # Se trocou a imagem, apaga o arquivo antigo da pasta media
        if nova_imagem and imagem_antiga and imagem_antiga.name != noticia.imagem.name:
            imagem_antiga.storage.delete(imagem_antiga.name)

    def perform_destroy(self, instance):
        instance.imagem.delete(save=False)  # Apaga a imagem da pasta media
        instance.delete()
