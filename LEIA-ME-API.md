# API REST de Notícias (Django REST Framework + Swagger)

Atende ao requisito: *"Uma entidade disponibilizada por API com Django REST Framework, contemplando consulta e criação de registros, validações, permissões pertinentes e documentação pelo Swagger/OpenAPI."*

A entidade é a **Notícia** (`noticias.models.Noticia`). Não houve mudança no model, então **não precisa de migration**.

## Arquivos

| Arquivo | Situação | O que faz |
|---|---|---|
| `noticias/noticias/serializers.py` | Novo | Converte Notícia ⇄ JSON e faz as validações |
| `noticias/noticias/api.py` | Novo | ViewSet com listar, consultar, criar, editar e excluir + textos do Swagger |
| `noticias/noticias/api_urls.py` | Novo | Rotas da API (router do DRF) |
| `noticias/noticias/tests.py` | Substituído | 16 testes automáticos da API |
| `noticias/siteweb/settings.py` | Alterado | `rest_framework`, `drf_spectacular` e `drf_spectacular_sidecar` no `INSTALLED_APPS` + blocos `REST_FRAMEWORK` e `SPECTACULAR_SETTINGS` no final |
| `noticias/siteweb/urls.py` | Alterado | Rotas `/api/`, `/api-auth/`, `/api/schema/`, `/api/docs/`, `/api/redoc/` |
| `requirements.txt` | Substituído | Em UTF-8, com DRF, drf-spectacular (+ sidecar) e as bibliotecas do clima |

## Instalação

```
pip install -r requirements.txt
cd noticias
python manage.py test noticias     # deve mostrar: Ran 16 tests ... OK
python manage.py runserver
```

O Swagger usa o `drf-spectacular-sidecar`: os arquivos dele ficam no próprio projeto, então a documentação abre mesmo sem internet.

## Endereços

| Endereço | O que é |
|---|---|
| `http://127.0.0.1:8000/api/docs/` | **Swagger** (documentação interativa) |
| `http://127.0.0.1:8000/api/redoc/` | Documentação no formato ReDoc |
| `http://127.0.0.1:8000/api/schema/` | Arquivo OpenAPI (YAML) |
| `http://127.0.0.1:8000/api/noticias/` | API navegável do DRF |

## Endpoints

| Método | URL | Ação | Quem pode |
|---|---|---|---|
| GET | `/api/noticias/` | Listar (paginado, 10 por página) | Qualquer visitante |
| GET | `/api/noticias/{id}/` | Consultar uma notícia | Qualquer visitante |
| POST | `/api/noticias/` | Criar | Permissão `noticias.add_noticia` |
| PUT | `/api/noticias/{id}/` | Editar todos os campos (imagem opcional) | Permissão `noticias.change_noticia` |
| PATCH | `/api/noticias/{id}/` | Editar só os campos enviados | Permissão `noticias.change_noticia` |
| DELETE | `/api/noticias/{id}/` | Excluir (apaga também a imagem) | Permissão `noticias.delete_noticia` |

Filtros na listagem: `?search=texto` (busca em título, fonte e texto) e `?ordering=data`, `-data`, `titulo`, `-titulo`.

## Permissões

Usa `DjangoModelPermissionsOrAnonReadOnly`: leitura liberada, e criar/editar/excluir exige as **mesmas permissões do Django** que as telas do site já usam (`permission_required`). Superusuário tem todas. Para um usuário comum, dê as permissões em **/admin → Usuários → Permissões do usuário** (ex.: "noticias | notícia | Can add noticia").

Sem login → 403. Logado sem permissão → 403.

## Validações

- **Título**: obrigatório, mínimo 5 caracteres.
- **Imagem**: obrigatória na criação, máximo 5 MB, precisa ser imagem válida. Na edição é opcional (mantém a atual); se trocar, a antiga é apagada da pasta media.
- **Data**: obrigatória, formato `AAAA-MM-DD`, não pode ser no futuro.
- **Fonte**: obrigatória.
- **Texto**: obrigatório, mínimo 20 caracteres.
- Não permite duas notícias com o **mesmo título na mesma data**.

Erros voltam com status **400** e a mensagem de cada campo, por exemplo:

```json
{
  "titulo": ["O título deve ter pelo menos 5 caracteres."],
  "data": ["A data da notícia não pode ser no futuro."]
}
```

## Roteiro para demonstrar no Swagger

1. Abra `/api/docs/` e execute **GET /api/noticias/** sem login → funciona (consulta aberta).
2. Tente **POST /api/noticias/** sem login → **403** (permissão).
3. Faça login: clique em **Authorize** → *basicAuth* → usuário e senha de um superusuário (ou entre antes por `/admin/` ou `/accounts/login/`, que o Swagger usa a mesma sessão).
4. **POST** com dados inválidos (título "Oi", data futura) → **400** com as mensagens (validações).
5. **POST** com dados corretos e uma imagem → **201** (criação).
6. **PATCH /api/noticias/{id}/** alterando só o título → **200** (edição).
7. **DELETE /api/noticias/{id}/** → **204** (exclusão).
