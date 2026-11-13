# SoftControl Brasil — Site (v2, Django)

Reformulação do site institucional da **SoftControl Brasil**, com o backend migrado de JavaScript para **Django** e um módulo de **notícias e artigos** com controle de visibilidade, categorias e API REST.

> Trabalho Final de Programação Web II.

## Funcionalidades

- Páginas institucionais: início, produtos, downloads, sobre e contato
- **Notícias:** listagem, leitura, cadastro, edição e exclusão, com upload de imagem
- **Visibilidade:** o usuário autorizado publica ou oculta notícias; o visitante vê apenas as publicadas
- **Categorias** com CRUD próprio, busca por texto e filtro por categoria
- Login e logout, com permissões verificadas no servidor
- **API REST** (Django REST Framework) com documentação **Swagger/OpenAPI**
- Widget de clima na página inicial (Open-Meteo, sem chave de API)

## Tecnologias

Python 3.12+ · Django 6.1 · Django REST Framework · drf-spectacular · SQLite · Bootstrap 5

## Como executar

```bash
git clone https://github.com/bbortolondasilva/reformulacao-site-v2.git
cd reformulacao-site-v2

python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate

pip install -r requirements.txt

cd noticias
python manage.py migrate
python manage.py runserver
```

Acesse http://127.0.0.1:8000/

## Testes

```bash
cd noticias
python manage.py test
```

## Endereços principais

| Endereço | Descrição |
|---|---|
| `/noticias/` | Lista pública de notícias (busca e filtro) |
| `/accounts/login/` | Login |
| `/admin/` | Django Admin |
| `/api/noticias/` | API de notícias |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |

## Perfis

| Perfil | Pode |
|---|---|
| Visitante | Ver notícias publicadas e consultar a API (somente leitura) |
| Administrador de conteúdo | Gerenciar notícias, visibilidade e categorias; usar a API com escrita |
| Superusuário | Acesso total, inclusive ao `/admin/` |

Para criar um superusuário: `python manage.py createsuperuser`.

## Autores

- [Bruno Bortolon](https://github.com/bbortolondasilva)
- [Filipe Zaffonato](https://github.com/Lico862)

## Licença

Veja o arquivo [LICENSE](LICENSE).
