# VibroSoft 

## Descripción
VibroSoft es una aplicación API REST basada en Django diseñada para manejar datos de series temporales con enfoque en la gestión de marcas de tiempo. El proyecto está especialmente diseñado para interactuar con dispositivos físicos de medición, recibiendo y procesando datos en tiempo real de estos equipos. La aplicación proporciona endpoints para registrar y recuperar información de fecha y hora, permitiendo un monitoreo efectivo y visualización de los datos recopilados por los dispositivos, haciéndolo ideal para aplicaciones de monitoreo industrial y registro de mediciones.

## Características 

- Endpoints API REST para gestión de fecha y hora
- Registro automático de marcas de tiempo
- Formato de respuesta JSON
- Construido con Django y Django REST Framework
- Interfaz de administración moderna usando Django Jazzmin
- Base de datos SQLite para almacenamiento

## Tecnologías Utilizadas 

- Python 3.x
- Django 5.1.5
- Django REST Framework 3.15.2
- Django Jazzmin 3.0.1
- CoreAPI para documentación de API
- SQLite como base de datos

## Instalación 

1. Clonar el repositorio
```bash
git clone [url-de-tu-repositorio]
cd vibrosoft
```

2. Crear y activar un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows usar: venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Ejecutar migraciones
```bash
python manage.py migrate
```

5. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```

## Endpoints de la API 

- `GET /api/datetime/` - Obtener todos los registros de tiempo
- `POST /api/datetime/` - Crear un nuevo registro de tiempo
- `GET /api/obtener-fecha-hora/` - Obtener fecha y hora actual

## Estructura del Proyecto 

```
vibrosoft/
├── api/                # Directorio principal de la aplicación
├── static/            # Archivos estáticos
├── templates/         # Plantillas HTML
├── vibrosoft/         # Configuración del proyecto
├── manage.py          # Script de gestión de Django
└── requirements.txt   # Dependencias del proyecto
```

## Contribuciones 

¡Las contribuciones, problemas y solicitudes de funciones son bienvenidas!

## Licencia 

[Tu Licencia Aquí]

---
Hecho con  usando Django y Python
