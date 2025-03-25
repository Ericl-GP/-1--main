from django.urls import path
from . import views

from .views import assetlinks, listar_notificacoes, marcar_como_lida
app_name = 'forum'

urlpatterns = [
    # URLs para sala
    path('sala/', views.sala_list, name='sala_list'),
    path('sala/create/', views.create_sala, name='create_sala'),
    path('sala/edit/<int:sala_id>/', views.edit_sala, name='edit_sala'),
    path('sala/delete/<int:sala_id>/', views.delete_sala, name='delete_sala'),

    # URLs para Categoria
    path('sala/<int:sala_id>/categoria/', views.categoria_list, name='categoria_list'),
    path('sala/<int:sala_id>/categoria/create/', views.create_categoria, name='create_categoria'),
    path('sala/<int:sala_id>/categoria/edit/<int:categoria_id>/', views.edit_categoria, name='edit_categoria'),
    path('sala/<int:sala_id>/categoria/delete/<int:categoria_id>/', views.delete_categoria, name='delete_categoria'),

    # URLs para Tópico
    path('categoria/<int:categoria_id>/topico/', views.topico_list, name='topico_list'),
    path('topico/<int:topico_id>/', views.topico_detail, name='topico_detail'),
    path('categoria/<int:categoria_id>/topico/create/', views.create_topico, name='create_topico'),
    path('topico/edit/<int:topico_id>/', views.edit_topico, name='edit_topico'),
    path('topico/delete/<int:topico_id>/', views.delete_topico, name='delete_topico'),

    # URLs para resposta
    path('topico/<int:topico_id>/resposta/add/', views.add_resposta, name='add_resposta'),
    path('resposta/edit/<int:resposta_id>/', views.edit_resposta, name='edit_resposta'),
    path('resposta/voto/<int:resposta_id>/', views.voto_resposta, name='voto_resposta'),
    path('resposta/delete/<int:resposta_id>/', views.delete_resposta, name='delete_resposta'),

    # URLs para tags
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.create_tag, name='create_tag'),
    path('tags/<int:tag_id>/delete/', views.delete_tag, name='delete_tag'),
    path('tags/<int:tag_id>/topicos/', views.topicos_by_tag, name='topicos_by_tag'),
    
    
    path('.well-known/assetlinks.json', assetlinks, name='assetlinks'),
    
    path('notificacoes/', listar_notificacoes, name='listar_notificacoes'),
    path('notificacoes/lida/<int:notificacao_id>/', marcar_como_lida, name='marcar_como_lida'),
    
    path('sobre/', views.sobre, name='sobre'),
]
