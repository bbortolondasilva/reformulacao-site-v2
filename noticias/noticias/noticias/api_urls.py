from rest_framework.routers import DefaultRouter

from .api import NoticiaViewSet

# O router cria automaticamente:
#   GET    /api/noticias/        -> listar
#   POST   /api/noticias/        -> criar
#   GET    /api/noticias/<id>/   -> consultar
#   PUT    /api/noticias/<id>/   -> editar (todos os campos)
#   PATCH  /api/noticias/<id>/   -> editar (campos parciais)
#   DELETE /api/noticias/<id>/   -> excluir
router = DefaultRouter()
router.register("noticias", NoticiaViewSet, basename="api-noticias")

urlpatterns = router.urls
