from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('ficheros_micro/<int:id>', views.ficheros_micro, name="ficheros_micro"),
    path('ver_contenido_archivo/<int:id>/<str:nombre_archivo>/', views.ver_contenido_archivo, name='ver_contenido_archivo'),
    path('descargar_archivo/<int:id>/<str:nombre_archivo>/', views.descargar_archivo, name='descargar_archivo'),
    path('update_config/<int:id>/', views.update_config, name='update_config'),
    path('descargar_archivos/<int:id>/', views.descargar_archivos, name='descargar_archivos'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.log_out, name="logout"), 
]
