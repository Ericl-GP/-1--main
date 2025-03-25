from django.db import models
from django.contrib.auth.models import User, Group

class Curso(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

# Modelo para Sala
class Sala(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cursos_permitidos = models.ManyToManyField(Curso, blank=True, related_name='salas')  # Cursos que podem acessar
    tipo_usuario_permitido = models.CharField(
        max_length=10,
        choices=[('ingresso', 'Ingresso'), ('egresso', 'Egresso')],
        blank=True,
        null=True
    )  # Tipo de usuário permitido
    publico = models.BooleanField(default=True)  # Define se é acessível a todos ou não

    def __str__(self):
        return self.name


# Modelo para Categoria (associada a Sala)
class Categoria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return self.name


# Modelo para Tag (associada a Tópicos)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Modelo para Tópico
class Topico(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='topicos')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, related_name="topicos", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Modelo para Resposta
class Resposta(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topico = models.ForeignKey(Topico, related_name='respostas', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    votos = models.IntegerField(default=0)  # Contador de votos

    def __str__(self):
        return f"Resposta para {self.topico.title}"


# Modelo para Voto
class Voto(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    resposta = models.ForeignKey('Resposta', on_delete=models.CASCADE, related_name='votos_relacionados')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resposta')

    def __str__(self):
        return f"Voto de {self.user.username if self.user else 'Desconhecido'} na resposta {self.resposta.id}"
    
    
#----------------------------------------------------------------------------------

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Notificacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, null=True, blank=True, related_name='notificacoes')
    resposta = models.ForeignKey(Resposta, on_delete=models.CASCADE, null=True, blank=True, related_name='notificacoes')

    def __str__(self):
        return f"Notificação para {self.user.username} - {'Lida' if self.lida else 'Não lida'}"


@receiver(post_save, sender=Resposta)
def criar_notificacao(sender, instance, created, **kwargs):
    if created:
        autor_topico = instance.topico.author
        if autor_topico and autor_topico != instance.author:
            mensagem = f"{instance.author.username} comentou no seu tópico '{instance.topico.title}'."
            Notificacao.objects.create(
                user=autor_topico,
                mensagem=mensagem,
                topico=instance.topico,
                resposta=instance
            )
