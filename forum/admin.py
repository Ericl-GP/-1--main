from django.contrib import admin
from .models import Curso, Sala, Categoria, Topico, Resposta, Voto

admin.site.register(Curso)
admin.site.register(Sala)
admin.site.register(Categoria)
admin.site.register(Topico)
admin.site.register(Resposta)
admin.site.register(Voto)