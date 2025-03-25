from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class GoogleForm(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    link_formulario = models.URLField()
    link_resultado = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('formulario_detalhe', kwargs={'form_id': self.id})
