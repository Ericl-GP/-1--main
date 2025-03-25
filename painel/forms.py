# forms.py
from django import forms
from .models import GoogleForm

class GoogleFormForm(forms.ModelForm):
    class Meta:
        model = GoogleForm
        fields = ['titulo', 'descricao', 'link_formulario', 'link_resultado']

    link_resultado = forms.URLField(
        required=False, 
        label="Link para Resultado", 
        widget=forms.URLInput(attrs={'placeholder': 'Opcional'})
    )
