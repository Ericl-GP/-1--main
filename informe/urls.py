from django.urls import path
from . import views

urlpatterns = [
    # Página de Informes
    path('informes/', views.informes, name='informes'),
    
    # URLs para Informes
    path('info/list/', views.info_list, name='info_list'),
    path('info/create/', views.info_create, name='info_create'),
    path('info/<int:info_id>/', views.info_detail, name='info_detail'),
    path('info/<int:info_id>/edit/', views.info_update, name='info_update'),
    path('info/<int:info_id>/delete/', views.info_delete, name='info_delete'),
    
    # URLs para Banners
    path('banner/list/', views.banner_list, name='banner_list'),
    path('banner/create/', views.banner_create, name='banner_create'),
    path('banner/<int:pk>/edit/', views.banner_update, name='banner_update'),
    path('banner/<int:pk>/delete/', views.banner_delete, name='banner_delete'),
]
