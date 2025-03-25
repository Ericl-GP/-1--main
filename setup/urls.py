from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contas.urls')),
    path('', include('forum.urls')),
    path('', include('informe.urls')),
    path('', include('painel.urls')),
]
# Adicione isso para servir arquivos estáticos em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Isso já está incluindo as mídias, mas faltava estáticos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)