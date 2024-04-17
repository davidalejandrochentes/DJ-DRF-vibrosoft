from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dispositivo
import requests
from django.http import JsonResponse
from django.urls import reverse
import zipfile
import io

@login_required
def home(request):
    dispositivos_activos = Dispositivo.objects.filter(activo=True)
    dispositivos_disponibles = []
    dispositivos_sin_respuesta_ok = []

    for dispositivo in dispositivos_activos:
        try:
            response = requests.get(dispositivo.url + "/ok?ok=ok")
            if response.status_code == 200:
                dispositivos_disponibles.append(dispositivo)
            else:
                dispositivos_sin_respuesta_ok.append(dispositivo)
        except Exception as e:
            # Agregar dispositivo a la lista si hay una excepción al hacer la solicitud
            dispositivos_sin_respuesta_ok.append(dispositivo)

    context = {
        'dispositivos_disponibles': dispositivos_disponibles,
        'dispositivos_sin_respuesta_ok': dispositivos_sin_respuesta_ok
    }
    return render(request, 'vibrotech/home.html', context)


@login_required
def ficheros_micro(request, id):
    micro = get_object_or_404(Dispositivo, id=id)
    try:
        response_files = requests.get(micro.url + "/files")
        if response_files.status_code == 200:
            archivos = response_files.json()  # Suponiendo que la respuesta es en formato JSON
            archivos.reverse()  # Invertir el orden de la lista de archivos
            archivos = [archivo for archivo in archivos if archivo != "data_config.txt"]  # Filtrar el archivo "data_config.txt"
        else:
            archivos = []  # Manejar el caso cuando no se puede obtener la lista de archivos
    except Exception as e:
        archivos = []  # Manejar el caso de excepción al hacer la solicitud

    try:
        response_capacity = requests.get(micro.url + "/capacity")
        if response_capacity.status_code == 200:
            capacity_data = response_capacity.json()
            total_bytes_gb = capacity_data.get("total_bytes_gb")
            used_bytes_mb = capacity_data.get("used_bytes_mb")
            free_bytes_gb = capacity_data.get("free_bytes_gb")
        else:
            total_bytes_gb = None
            used_bytes_mb = None
            free_bytes_gb = None
    except Exception as e:
        total_bytes_gb = None
        used_bytes_mb = None
        free_bytes_gb = None

    context = {
        'micro': micro,
        'archivos': archivos,
        'total_bytes_gb': total_bytes_gb,
        'used_bytes_mb': used_bytes_mb,
        'free_bytes_gb': free_bytes_gb
    }
    return render(request, 'vibrotech/ficheros_micro.html', context)



@login_required
def ver_contenido_archivo(request, id, nombre_archivo):
    micro = get_object_or_404(Dispositivo, id=id)
    
    try:
        response = requests.get(f"{micro.url}/file?file={nombre_archivo}")
        if response.status_code == 200:
            data = response.json()
            return render(request, 'vibrotech/contenido_archivo.html', {'micro': micro, 'archivo': data})
        else:
            return render(request, 'vibrotech/error.html', {'mensaje': 'No se pudo obtener el contenido del archivo'})
    except Exception as e:
        return render(request, 'vibrotech/error.html', {'mensaje': 'Error al obtener el contenido del archivo'})


@login_required
def update_config(request, id):
    if request.method == 'POST':
        # Obtener el dispositivo
        micro = get_object_or_404(Dispositivo, id=id)

        # Obtener los datos del formulario
        samples = request.POST.get('samples')
        interval_value = request.POST.get('interval')
        unit = int(request.POST.get('time'))  # Obtener la unidad seleccionada desde el formulario

        # Convertir el intervalo a segundos según la unidad seleccionada
        interval = int(interval_value) * int(unit)

        # Construir la URL con los parámetros
        url = f"{micro.url}/update_config?samples={samples}&interval={interval}"

        try:
            # Realizar la solicitud POST al dispositivo
            response = requests.post(url)
            if response.status_code == 200:
                # Redireccionar a la página actual
                return redirect(request.META.get('HTTP_REFERER', 'home'))
            else:
                return JsonResponse({'error': 'Hubo un problema al actualizar la configuración'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Error al comunicarse con el dispositivo'}, status=500)


@login_required
def descargar_archivo(request, id, nombre_archivo):
    micro = get_object_or_404(Dispositivo, id=id)
    
    try:
        response = requests.get(f"{micro.url}/file?file={nombre_archivo}")
        if response.status_code == 200:
            contenido = response.json()['file_content']
            response = HttpResponse(contenido, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return response
        else:
            return render(request, 'vibrotech/error.html', {'mensaje': 'No se pudo obtener el contenido del archivo'})
    except Exception as e:
        return render(request, 'vibrotech/error.html', {'mensaje': 'Error al obtener el contenido del archivo'})


@login_required
def descargar_archivos(request, id):
    micro = get_object_or_404(Dispositivo, id=id)
    
    try:
        response_files = requests.get(micro.url + "/files")
        if response_files.status_code == 200:
            archivos = response_files.json()  # Suponiendo que la respuesta es en formato JSON
            contenido_zip = io.BytesIO()
            with zipfile.ZipFile(contenido_zip, 'w') as zip_file:
                for archivo in archivos:
                    response = requests.get(f"{micro.url}/file?file={archivo}")
                    if response.status_code == 200:
                        data = response.json()
                        file_content = data.get('file_content')
                        if file_content:
                            # Modificar el contenido para separar cada número por una nueva línea
                            file_content = file_content.replace(',', '\n')
                            # Escribir el contenido modificado en el archivo ZIP
                            zip_file.writestr(archivo, file_content)
                    else:
                        return render(request, 'vibrotech/ficheros_micro.html', {'mensaje': f'Error al obtener el contenido del archivo {archivo}'})
            contenido_zip.seek(0)
            response = HttpResponse(contenido_zip, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{micro.nombre}_archivos.zip"'
            return response
        else:
            return render(request, 'vibrotech/ficheros_micro.html', {'mensaje': 'No se pudo obtener la lista de archivos'})
    except Exception as e:
        return render(request, 'vibrotech/ficheros_micro.html', {'mensaje': 'Error al obtener la lista de archivos'})




def login_view(request):
    if request.method =='GET':
        context = {}
        return render (request, 'vibrotech/login.html', context) 
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.success(request, "El usuario no existe, o la password es incorrecta")
            return render(request, 'vibrotech/login.html', {})
        else:
            login(request, user)
            return redirect('home')


@login_required
def log_out(request):
    logout(request)
    return redirect('home')     