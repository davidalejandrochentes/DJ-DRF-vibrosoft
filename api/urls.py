from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'datatime', views.DataTimeMicroViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('obtener-fecha-hora/', views.obtener_fecha_hora, name='obtener_fecha_hora'),
]