from django import forms
from .models import Info, Banner

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['title', 'url', 'description']
        

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image', 'link']