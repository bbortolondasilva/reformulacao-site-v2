import io
import shutil
import tempfile
from datetime import date, timedelta

from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Noticia

MEDIA_TESTE = tempfile.mkdtemp()  # Pasta temporária para as imagens dos testes


def gerar_imagem(nome="teste.png"):
    arquivo = io.BytesIO()
    Image.new("RGB", (10, 10), "green").save(arquivo, "PNG")
    return SimpleUploadedFile(nome, arquivo.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=MEDIA_TESTE)
class NoticiaAPITests(APITestCase):
    url_lista = "/api/noticias/"

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TESTE, ignore_errors=True)

    def setUp(self):
        self.noticia = Noticia.objects.create(
            titulo="Notícia existente",
            imagem=gerar_imagem(),
            data=date.today(),
            fonte="SoftControl",
            texto="Texto da notícia que já existe no banco de dados.",
        )
        self.url_detalhe = f"/api/noticias/{self.noticia.pk}/"

        # Usuário com todas as permissões de notícia
        self.editor = User.objects.create_user("editor", password="senha123")
        self.editor.user_permissions.add(
            *Permission.objects.filter(codename__in=[
                "add_noticia", "change_noticia", "delete_noticia", "view_noticia",
            ])
        )
        # Usuário logado, mas sem permissões
        self.comum = User.objects.create_user("comum", password="senha123")

    def dados_validos(self, **extras):
        dados = {
            "titulo": "Nova notícia da API",
            "imagem": gerar_imagem(),
            "data": date.today().isoformat(),
            "fonte": "https://www.softcontrol.com.br",
            "texto": "Conteúdo da notícia criada pela API REST.",
        }
        dados.update(extras)
        return dados

    # ---------- Consulta ----------

    def test_visitante_lista_noticias(self):
        resposta = self.client.get(self.url_lista)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["count"], 1)

    def test_visitante_consulta_uma_noticia(self):
        resposta = self.client.get(self.url_detalhe)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["titulo"], "Notícia existente")

    # ---------- Criação e permissões ----------

    def test_visitante_nao_cria(self):
        resposta = self.client.post(self.url_lista, self.dados_validos(), format="multipart")
        self.assertIn(resposta.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_usuario_sem_permissao_nao_cria(self):
        self.client.force_authenticate(self.comum)
        resposta = self.client.post(self.url_lista, self.dados_validos(), format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_cria_noticia(self):
        self.client.force_authenticate(self.editor)
        resposta = self.client.post(self.url_lista, self.dados_validos(), format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED, resposta.data)
        self.assertEqual(Noticia.objects.count(), 2)

    # ---------- Validações ----------

    def test_data_futura_invalida(self):
        self.client.force_authenticate(self.editor)
        amanha = (date.today() + timedelta(days=1)).isoformat()
        resposta = self.client.post(self.url_lista, self.dados_validos(data=amanha), format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("data", resposta.data)

    def test_titulo_curto_invalido(self):
        self.client.force_authenticate(self.editor)
        resposta = self.client.post(self.url_lista, self.dados_validos(titulo="Oi"), format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", resposta.data)

    def test_texto_curto_invalido(self):
        self.client.force_authenticate(self.editor)
        resposta = self.client.post(self.url_lista, self.dados_validos(texto="curto"), format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("texto", resposta.data)

    def test_titulo_repetido_na_mesma_data_invalido(self):
        self.client.force_authenticate(self.editor)
        resposta = self.client.post(
            self.url_lista, self.dados_validos(titulo="notícia EXISTENTE"), format="multipart"
        )
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_imagem_obrigatoria_na_criacao(self):
        self.client.force_authenticate(self.editor)
        dados = self.dados_validos()
        dados.pop("imagem")
        resposta = self.client.post(self.url_lista, dados, format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("imagem", resposta.data)

    # ---------- Edição ----------

    def test_editor_edita_parcialmente(self):
        self.client.force_authenticate(self.editor)
        resposta = self.client.patch(self.url_detalhe, {"titulo": "Título alterado"}, format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK, resposta.data)
        self.noticia.refresh_from_db()
        self.assertEqual(self.noticia.titulo, "Título alterado")

    def test_put_sem_imagem_mantem_a_atual(self):
        self.client.force_authenticate(self.editor)
        imagem_antes = self.noticia.imagem.name
        dados = self.dados_validos()
        dados.pop("imagem")
        resposta = self.client.put(self.url_detalhe, dados, format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK, resposta.data)
        self.noticia.refresh_from_db()
        self.assertEqual(self.noticia.imagem.name, imagem_antes)

    def test_usuario_sem_permissao_nao_edita(self):
        self.client.force_authenticate(self.comum)
        resposta = self.client.patch(self.url_detalhe, {"titulo": "Tentativa"}, format="multipart")
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- Exclusão ----------

    def test_editor_exclui_noticia_e_imagem(self):
        self.client.force_authenticate(self.editor)
        storage, nome = self.noticia.imagem.storage, self.noticia.imagem.name
        resposta = self.client.delete(self.url_detalhe)
        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Noticia.objects.exists())
        self.assertFalse(storage.exists(nome))

    def test_usuario_sem_permissao_nao_exclui(self):
        self.client.force_authenticate(self.comum)
        resposta = self.client.delete(self.url_detalhe)
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Noticia.objects.exists())

    # ---------- Documentação ----------

    def test_swagger_e_schema_disponiveis(self):
        self.assertEqual(self.client.get("/api/docs/").status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get("/api/schema/").status_code, status.HTTP_200_OK)
