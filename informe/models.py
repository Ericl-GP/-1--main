from django.db import models
from django.conf import settings
from django.urls import reverse
import os
class Info(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('info_detail', kwargs={'pk': self.pk})
#------------------------------------------------------------

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    link = models.URLField()

    def __str__(self):
        return f"Banner {self.id}"

    def save(self, *args, **kwargs):
        # Se o banner já existe (está sendo editado)
        if self.pk:
            # Obter o banner antigo (caso exista)
            old_banner = Banner.objects.get(pk=self.pk)
            # Se a imagem foi alterada, apague a imagem anterior
            if old_banner.image != self.image:
                if old_banner.image:
                    old_image_path = os.path.join(settings.MEDIA_ROOT, str(old_banner.image))
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
        
        # Chama o método save original para salvar o objeto
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Excluir a imagem quando o banner for deletado
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
            if os.path.isfile(image_path):
                os.remove(image_path)
        
        # Chama o método delete original para excluir o objeto
        super().delete(*args, **kwargs)