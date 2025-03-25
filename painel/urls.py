from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('formulario_lista/', views.form_list, name='formulario_lista'),
    path('formulario/<int:form_id>/', views.form_detail, name='formulario_detalhe'),
    path('formulario/criar/', views.form_create, name='formulario_criar'),
    path('formulario/atualizar/<int:form_id>/', views.form_update, name='formulario_atualizar'),
    path('formulario/deletar/<int:form_id>/', views.form_delete, name='formulario_deletar'),
]
