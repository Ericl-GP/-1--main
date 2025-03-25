from django import forms
from .models import Sala, Categoria, Topico, Resposta, Tag
from django.contrib.auth.models import User, Group
from forum.models import Curso

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['name', 'description', 'cursos_permitidos', 'tipo_usuario_permitido', 'publico']

    # Adicionando campos para selecionar cursos e tipo de usuário
    cursos_permitidos = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(), 
        required=False,
        widget=forms.CheckboxSelectMultiple(), 
        label="Cursos Permitidos"
    )
    tipo_usuario_permitido = forms.ChoiceField(
        choices=[('', 'Qualquer tipo'), ('ingresso', 'Ingresso'), ('egresso', 'Egresso')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de Usuário Permitido"
    )
    publico = forms.BooleanField(
        required=False,
        initial=True,
        label="Público",
        help_text="Marque para permitir que qualquer usuário tenha acesso à Sala."
    )


# Formulário para Categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['name', 'description']


class TopicoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tags"
    )

    class Meta:
        model = Topico
        fields = ['title', 'content', 'tags']


# Formulário para Resposta
class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['content']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']