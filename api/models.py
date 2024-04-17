from django.db import models
from datetime import date
from datetime import datetime

# Create your models here.
class DataTimeMicro(models.Model):
    fecha = models.DateField(auto_now_add=True),
    hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        txt = "Fecha: {}, Hora: {}"
        return txt.format(self.fecha, self.hora)    