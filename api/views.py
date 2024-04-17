from rest_framework import viewsets
from .serializer import DataTimeMicroSerializer
from .models import DataTimeMicro

from django.http import JsonResponse
from datetime import datetime

# Create your views here.

class DataTimeMicroViewSet(viewsets.ModelViewSet):
    queryset = DataTimeMicro.objects.all()
    serializer_class = DataTimeMicroSerializer

def obtener_fecha_hora(request):
    fecha_hora_actual = {
        'fecha': datetime.now().strftime('%Y-%m-%d'),
        'hora': datetime.now().strftime('%H:%M:%S')
    }
    return JsonResponse(fecha_hora_actual)
