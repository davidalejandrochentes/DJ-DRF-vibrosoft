from django.db import models

# Create your models here.
class Dispositivo(models.Model):
    url = models.URLField(unique=True, blank=False, null=False)
    activo = models.BooleanField(default=False)
    nombre = models.CharField(max_length=20, blank=False, null=False)
    localidad = models.CharField(max_length=20, blank=True, null=True)
    descripción = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre