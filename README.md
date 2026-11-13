# SoftControl Brasil — Notícias e Artigos

**Trabalho Final — Programação Web II**
Transição de backend (JS → Django) e implementação da página de notícias e artigos do site da SoftControl Brasil.

**Integrantes:** Bruno Bortolon da Silva e Filipe Zaffonato
**Repositório:** https://github.com/bbortolondasilva/reformulacao-site-v2

---

## 1. Descrição do sistema

O projeto dá continuidade ao site institucional desenvolvido em Programação Web I. O backend, que antes era em JavaScript, foi reescrito em **Django**, e foi implementado o módulo que ainda não existia na reformulação: **notícias e artigos**.

**Problema que resolve:** a empresa precisa publicar notícias do ramo empresarial no próprio site, controlando quais ficam visíveis ao público, sem depender de edição manual de páginas.

**Público-alvo:** visitantes do site (leitura) e a equipe da empresa autorizada a gerenciar o conteúdo.

**Fluxo prioritário (conforme o escopo pactuado):** um usuário autorizado gerencia notícias e a visibilidade delas; o visitante visualiza somente as publicadas. Categorias complementam os relacionamentos e os filtros.

## 2. Perfis de usuário e permissões

| Perfil | Como acessa | O que pode fazer |
|---|---|---|
| **Visitante** | Sem login | Ver notícias **publicadas**, buscar e filtrar por categoria, consultar a API em modo leitura |
| **Administrador de conteúdo** | Login (grupo "Administradores") | Tudo do visitante, mais: ver rascunhos, criar/editar/excluir notícias, publicar/ocultar (campo "Publicada"), gerenciar categorias, usar a API com escrita |
| **Superusuário** | Login + Django Admin | Acesso total, inclusive ao `/admin/` |

As permissões usam o sistema nativo do Django (`add_`, `change_`, `delete_`, `view_`) e são **verificadas no servidor** (decorators nas views e permissões do DRF na API). Ocultar um botão no template é apenas um recurso visual.

### Usuários de demonstração

| Usuário | Senha | Perfil |
|---|---|---|
| `jovania` | `[PREENCHER: senha de demonstração]` | Administrador de conteúdo (grupo "Administradores") |
| *(sem login)* | — | Visitante |

O usuário `jovania` não é superusuário e não acessa o Django Admin; ele serve para testar as telas do site e a API com permissões de gerenciamento. Para criar outros usuários, veja a seção 6.

## 3. Funcionalidades

| Funcionalidade | Situação |
|---|---|
| Listar notícias (mais recentes primeiro) | Concluída |
| Visualizar notícia, com navegação anterior/próxima | Concluída |
| Cadastrar, editar e excluir notícias (com imagem) | Concluída |
| Visibilidade: campo "Publicada" no formulário; visitante só vê as publicadas | Concluída |
| Rascunhos identificados para o usuário autorizado | Concluída |
| Categorias: cadastro, edição e exclusão em páginas próprias | Concluída |
| Busca por título/texto e filtro por categoria | Concluída |
| Login e logout | Concluída |
| API REST de notícias (listar, consultar, criar, editar, excluir) | Concluída |
| Documentação Swagger/OpenAPI e ReDoc | Concluída |
| Testes automatizados da API | Concluída |
| Testes automatizados das telas do site | `[PREENCHER: Concluída / Parcial]` |
| Widget de clima na página inicial (Open-Meteo) | Concluída (depende de internet) |
| Cadastro de usuários pelo site | Não implementado (usa-se o Django Admin) |

### Regras de negócio

1. **Visibilidade:** o visitante nunca recebe uma notícia não publicada, nem pela lista, nem pela URL direta (404), nem pelos botões anterior/próxima, nem pela API.
2. **Categoria protegida:** não é possível excluir uma categoria que ainda tenha notícias associadas (o sistema exibe uma mensagem e mantém os dados).
3. **Nome de categoria único**, sem diferenciar maiúsculas de minúsculas.
4. **API:** não aceita duas notícias com o mesmo título na mesma data.

### Limitações conhecidas

- O cadastro de novos usuários é feito pelo Django Admin; não há página de registro no site.
- Cada notícia pertence a, no máximo, uma categoria.
- O widget de clima precisa de acesso à internet; sem conexão, o site funciona e exibe uma mensagem no lugar da temperatura.
- O projeto usa SQLite e configurações de desenvolvimento (`DEBUG = True`); não está preparado para produção.
- As imagens enviadas ficam no disco local (`media/`).

## 4. Tecnologias

- Python 3.12 ou superior
- Django 6.1
- Django REST Framework 3.18 e drf-spectacular (Swagger/OpenAPI)
- SQLite
- Bootstrap 5 (via CDN) e CSS próprio
- Pillow (upload de imagens)
- Open-Meteo (clima, **sem necessidade de chave de API**)

## 5. Instalação e execução

### 5.1. Pré-requisitos

- Python 3.12 ou superior (`python --version`)
- Git (opcional, se for usar o repositório em vez do arquivo compactado)

### 5.2. Passo a passo

```bash
# 1. Obtenha o código (repositório ou arquivo compactado)
git clone https://github.com/bbortolondasilva/reformulacao-site-v2.git
cd reformulacao-site-v2

# 2. Crie e ative um ambiente virtual
python -m venv venv

# Windows (PowerShell / CMD):
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Entre na pasta do projeto Django (onde está o manage.py)
cd noticias

# 5. Aplique as migrations
python manage.py migrate

# 6. Inicie o servidor
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/**.

> O arquivo `db.sqlite3` já acompanha o projeto, com notícias, categorias, o grupo "Administradores" e o usuário de demonstração. O `migrate` do passo 5 apenas garante que o banco esteja atualizado.

### 5.3. Executar os testes

Dentro da pasta `noticias/`:

```bash
python manage.py test
```

O resultado esperado é `OK`.

### 5.4. Configuração e credenciais

Não há credenciais reais nem chaves de serviços externos no código. O projeto usa uma `SECRET_KEY` de desenvolvimento e a API de clima (Open-Meteo) não exige chave.

## 6. Dados de demonstração e criação de usuários

### 6.1. Banco já preparado

Se o `db.sqlite3` entregue for usado, nada precisa ser feito: o login `jovania` já funciona.

### 6.2. Recriar do zero (caso apague o banco)

```bash
python manage.py migrate
python manage.py createsuperuser     # cria um superusuário (acessa /admin/)
python manage.py shell
```

No shell, cole o trecho abaixo para criar o grupo e um usuário administrador de conteúdo:

```python
from django.contrib.auth.models import User, Group, Permission

grupo, _ = Group.objects.get_or_create(name="Administradores")
grupo.permissions.set(
    Permission.objects.filter(content_type__model__in=["noticia", "categoria"])
)

usuario = User.objects.create_user("jovania", password="TROQUE-A-SENHA")
usuario.groups.add(grupo)
```

Depois, entre em `/admin/` com o superusuário e cadastre algumas categorias e notícias, ou use a própria interface do site com o usuário `jovania`.

## 7. Mapa de endereços

### Site

| Endereço | Descrição | Acesso |
|---|---|---|
| `/` | Página inicial | Público |
| `/produtos/`, `/downloads/`, `/sobre/`, `/contato/` | Páginas institucionais | Público |
| `/accounts/login/` | Login | Público |
| `/noticias/` | Lista de notícias, com busca e filtro (`?q=...&categoria=...`) | Público (só publicadas) |
| `/noticias/<id>/` | Notícia completa | Público (só publicadas) |
| `/noticias/criar-noticia/` | Cadastrar notícia | Permissão `add_noticia` |
| `/noticias/<id>/editar-noticia/` | Editar notícia e visibilidade | Permissão `change_noticia` |
| `/noticias/<id>/excluir/` | Excluir notícia (POST) | Permissão `delete_noticia` |
| `/noticias/categorias/` | Gerenciar categorias | Permissões de `categoria` |
| `/admin/` | Django Admin | Superusuário |

O logout é feito pelo botão "Sair" do menu (requisição POST).

### API e documentação

| Endereço | Descrição |
|---|---|
| `/api/docs/` | **Swagger UI** (documentação interativa) |
| `/api/redoc/` | Documentação em ReDoc |
| `/api/schema/` | Arquivo OpenAPI |
| `/api/noticias/` | API navegável do DRF |

## 8. API REST de notícias

| Método | Endpoint | Ação | Quem pode |
|---|---|---|---|
| GET | `/api/noticias/` | Listar (paginado, 10 por página) | Qualquer visitante (só publicadas) |
| GET | `/api/noticias/{id}/` | Consultar | Qualquer visitante (só publicadas) |
| POST | `/api/noticias/` | Criar | Permissão `add_noticia` |
| PUT / PATCH | `/api/noticias/{id}/` | Editar | Permissão `change_noticia` |
| DELETE | `/api/noticias/{id}/` | Excluir | Permissão `delete_noticia` |

Parâmetros da listagem: `?search=texto` (título, fonte e texto) e `?ordering=data`, `-data`, `titulo`, `-titulo`.

**Validações:** título com pelo menos 5 caracteres; texto com pelo menos 20; data obrigatória e não futura; fonte obrigatória; imagem obrigatória na criação, de até 5 MB e válida; título único por data. Erros retornam **400** com a mensagem de cada campo. Sem login ou sem permissão, a escrita retorna **403**.

## 9. Roteiro sugerido para a apresentação

**Fluxo completo no site**

1. Como visitante, abra `/noticias/`: apenas as notícias publicadas aparecem.
2. Busque por uma palavra e filtre por categoria.
3. Faça login com `jovania`.
4. Cadastre uma notícia **sem** marcar "Publicada": ela aparece com o selo de rascunho para o usuário logado.
5. Saia da conta e confirme que a notícia não aparece para o visitante (e que a URL direta retorna 404).
6. Entre novamente, edite a notícia, marque "Publicada" e confirme que o visitante passa a vê-la.

**Validação de dados:** tente cadastrar um formulário incompleto ou repetir o nome de uma categoria.

**Restrição de acesso:** sem login, acesse `/noticias/criar-noticia/` ou `/noticias/categorias/`.

**API no Swagger (`/api/docs/`)**

1. `GET /api/noticias/` sem login: funciona (só publicadas).
2. `POST /api/noticias/` sem login: **403**.
3. Em *Authorize*, informe `jovania` e a senha (ou faça login antes em `/accounts/login/`).
4. `POST` com título curto e data futura: **400** com as mensagens.
5. `POST` com dados válidos e imagem: **201**.
6. `PATCH` alterando só o título: **200**.
7. `DELETE`: **204**.

## 10. Organização do projeto

```
reformulacao-site-v2/
├── README.md
├── requirements.txt
└── noticias/                  # projeto Django (onde está o manage.py)
    ├── manage.py
    ├── db.sqlite3             # banco de demonstração
    ├── siteweb/               # configurações e URLs principais
    ├── base/                  # páginas institucionais, login e template base
    ├── noticias/              # app de notícias
    │   ├── models.py          # Noticia e Categoria
    │   ├── forms.py           # ModelForms e validações
    │   ├── views.py           # telas do site (CRUD, filtro, visibilidade)
    │   ├── urls.py            # rotas do site
    │   ├── serializers.py     # serializers da API
    │   ├── api.py             # ViewSet da API
    │   ├── api_urls.py        # rotas da API
    │   ├── tests.py           # testes automatizados
    │   └── templates/
    ├── clima_api/             # serviço de clima (Open-Meteo)
    ├── static/                # CSS, imagens e scripts
    └── media/                 # imagens enviadas nas notícias
```

## 11. Contribuição dos integrantes

> `[AJUSTAR]` O quadro abaixo é um rascunho. Revise conforme a divisão real das atividades; o histórico de commits do repositório complementa este registro.

| Integrante | Atividades |
|---|---|
| **Bruno Bortolon da Silva** | `[AJUSTAR]` Migração do backend para Django; app de notícias (models, views, formulários e templates); login/logout; autorização por permissões; visibilidade das notícias; ajustes de layout e CSS |
| **Filipe Zaffonato** | `[AJUSTAR]` Integração da API de clima; API REST de notícias com DRF e documentação Swagger; testes automatizados da API |

## 12. Uso de ferramentas de apoio

> `[CONFIRMAR]` Declare aqui, com suas palavras, o que foi usado. Sugestão de texto:

Durante o desenvolvimento foram utilizados Bootstrap, a documentação oficial do Django e do Django REST Framework e uma ferramenta de IA (Claude, da Anthropic) como apoio para revisar o projeto em relação aos critérios de avaliação e orientar a implementação de funcionalidades (visibilidade das notícias, categorias, filtros e API). O grupo testou o resultado e consegue explicar e modificar o código entregue.

## 13. Licença

Veja o arquivo `LICENSE` na raiz do repositório.
