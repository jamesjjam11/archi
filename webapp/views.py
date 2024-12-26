from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from .forms import UserCreationForm, CustomUserCreationForm, SecretariaForm, UnidadForm, UsuarioCargoUnidadForm, PersonaForm, CargoForm
from .models import Persona, Secretaria, Unidad, Cargo, UsuarioCargoUnidad, User, Bitacora
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed, FileResponse
from django.utils import timezone
from docx import Document
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import crear_superusuario_y_datos_por_defecto
from django.db.models import Q
import logging, os, subprocess, datetime, shutil
from pathlib import Path
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
User = get_user_model()

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'login/login.html', {'form': form})
class LogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return redirect('login')
@never_cache
@login_required
def index(request):
    user_roles = request.user.groups.values_list('name', flat=True)
    imagen_url = None  # Inicializamos como None

    try:
        # Intenta obtener la instancia de Persona
        persona = Persona.objects.get(user=request.user)
        if persona.image:  # Verifica si hay una imagen asociada
            imagen_url = persona.image.url
    except Persona.DoesNotExist:
        # Manejo si la Persona no existe
        imagen_url = None  # O usar una imagen por defecto
    except Exception as e:
        print(f"Error al acceder a la imagen: {e}")  # Captura cualquier otro error

    context = {
        'user_roles': user_roles,
        'imagen_url': imagen_url,  # Pasamos la URL de la imagen al contexto
    }
    return render(request, 'user/index.html', context)
@never_cache
@login_required
def register_user(request):
    form = CustomUserCreationForm()
    usuario_cargo_unidad_form = UsuarioCargoUnidadForm()
    persona_form = PersonaForm()
    secretaria_form = SecretariaForm()
    unidad_form = UnidadForm()
    cargo_form = CargoForm()

    context = {
        'persona_form': persona_form,
        'form': form,
        'usuario_cargo_unidad_form': usuario_cargo_unidad_form,
        'secretaria_form': secretaria_form,
        'unidad_form': unidad_form,
        'cargo_form': cargo_form,
        'user_roles': request.user_roles,
    }

    if request.method == 'POST':
        # Registro de usuario
        if 'submit_user' in request.POST:
            form = CustomUserCreationForm(request.POST, request.FILES)
            usuario_cargo_unidad_form = UsuarioCargoUnidadForm(request.POST)
            persona_form = PersonaForm(request.POST, request.FILES)

            if form.is_valid() and usuario_cargo_unidad_form.is_valid() and persona_form.is_valid():
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.save()

                persona = Persona(
                    user=user,
                    nombre=persona_form.cleaned_data['nombre'].upper(), 
                    apellido_paterno=persona_form.cleaned_data['apellido_paterno'].upper(),  
                    apellido_materno=persona_form.cleaned_data['apellido_materno'].upper(),  
                    ci=persona_form.cleaned_data['ci'].upper(),  
                    image=persona_form.cleaned_data['image'] if 'image' in request.FILES else None
                )
                persona.save()

                role = form.cleaned_data['roles']
                user.groups.add(role)

                usuario_cargo_unidad = usuario_cargo_unidad_form.save(commit=False)
                usuario_cargo_unidad.user = user
                usuario_cargo_unidad.fecha_inicio = timezone.now().date()
                usuario_cargo_unidad.save()

                messages.success(request, 'Usuario registrado correctamente')
                
                # Redirigir a la página de edición
                return redirect('viewUser', user_id=user.id)

            else:
                errors = {
                    'form': form.errors,
                    'usuario_cargo_unidad_form': usuario_cargo_unidad_form.errors,
                    'persona_form': persona_form.errors,
                }
                for error in errors.values():
                    for e in error:
                        messages.error(request, e)

        # Registro de Secretaría
        elif 'submit_secretaria' in request.POST:
            secretaria_form = SecretariaForm(request.POST)
            if secretaria_form.is_valid():
                try:
                    secretaria = secretaria_form.save(commit=False)
                    secretaria.nombre_secretaria = secretaria_form.cleaned_data['nombre_secretaria'].upper() 
                    secretaria.save()
                    messages.success(request, 'Secretaría registrada correctamente')
                except KeyError as e:
                    messages.error(request, f'Error: El campo {e} no fue encontrado en el formulario de Secretaría.')
            else:
                messages.error(request, 'Error al registrar la Secretaría.')

        # Registro de Unidad
        elif 'submit_unidad' in request.POST:
            unidad_form = UnidadForm(request.POST)
            if unidad_form.is_valid():
                try:
                    unidad = unidad_form.save(commit=False)
                    unidad.nombre_unidad = unidad_form.cleaned_data['nombre_unidad'].upper()  
                    unidad.save()
                    messages.success(request, 'Unidad registrada correctamente')
                except KeyError as e:
                    messages.error(request, f'Error: El campo {e} no fue encontrado en el formulario de Unidad.')
            else:
                messages.error(request, 'Error al registrar la Unidad.')

        # Registro de Cargo
        elif 'submit_cargo' in request.POST:
            cargo_form = CargoForm(request.POST)
            if cargo_form.is_valid():
                try:
                    cargo = cargo_form.save(commit=False)
                    cargo.nombre_cargo = cargo_form.cleaned_data['nombre_cargo'].upper()
                    cargo.save()
                    messages.success(request, 'Cargo registrado correctamente')
                except KeyError as e:
                    messages.error(request, f'Error: El campo {e} no fue encontrado en el formulario de Cargo.')
            else:
                messages.error(request, 'Error al registrar el Cargo.')

    return render(request, 'user/registerUser.html', context)


@never_cache
@login_required
def list_user(request):
    query = request.GET.get('q', '')
    usuarios = User.objects.filter(is_active=True).select_related('persona').prefetch_related('groups')

    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(persona__nombre__icontains=query) |
            Q(persona__apellido_paterno__icontains=query) |
            Q(persona__ci__icontains=query)
        )

    # Paginación
    paginator = Paginator(usuarios, 4)  # 4 usuarios por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la consulta
    try:
        usuarios_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        usuarios_paginated = paginator.page(1)  # Si no es un entero, muestra la primera página
    except EmptyPage:
        usuarios_paginated = paginator.page(paginator.num_pages)  # Si la página está vacía, muestra la última página

    usuario_cargo_unidad = UsuarioCargoUnidad.objects.select_related(
        'nombre_cargo', 
        'nombre_unidad__nombre_secretaria'
    ).all()

    context = {
        'usuarios': usuarios_paginated,  # Cambia esto a la lista paginada
        'usuario_cargo_unidad': usuario_cargo_unidad,
        'query': query  # Para mantener el valor de búsqueda en el campo de búsqueda
    }

    return render(request, 'user/listUser.html', context)

@never_cache
@login_required
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    try:
        persona = user.persona  # Suponiendo que tienes una relación OneToOne con el modelo Persona
    except User.persona.RelatedObjectDoesNotExist:
        persona = None

    try:
        usuario_cargo_unidad = user.usuariocargounidad  # Suponiendo que tienes una relación OneToOne con el modelo UsuarioCargoUnidad
    except User.usuariocargounidad.RelatedObjectDoesNotExist:
        usuario_cargo_unidad = None

    # Verifica si 'persona' tiene una imagen asociada
    if persona and persona.image:  # Asumiendo que el campo de imagen está en el modelo Persona
        user_image = persona.image.url
    else:
        user_image = '/static/images/blank-profile.png'  # Imagen en blanco o predeterminada

    context = {
        'user': user,
        'persona': persona,
        'usuario_cargo_unidad': usuario_cargo_unidad,
        'user_image': user_image,
    }
    return render(request, 'user/viewUser.html', context)


@never_cache
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    persona = get_object_or_404(Persona, user=user)
    usuario_cargo_unidad = get_object_or_404(UsuarioCargoUnidad, user=user)

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, instance=user)
        persona_form = PersonaForm(request.POST, request.FILES, instance=persona)
        ucu_form = UsuarioCargoUnidadForm(request.POST, instance=usuario_cargo_unidad)

        if user_form.is_valid() and persona_form.is_valid() and ucu_form.is_valid():
            user_form.save()
            persona_form.save()
            ucu_form.save()
            return redirect('viewUser', user_id=user.id)
    else:
        user_form = CustomUserCreationForm(instance=user)
        persona_form = PersonaForm(instance=persona)
        ucu_form = UsuarioCargoUnidadForm(instance=usuario_cargo_unidad)

    context = {
        'user_form': user_form,
        'persona_form': persona_form,
        'ucu_form': ucu_form,
        'user_id': user.id,
    }
    return render(request, 'user/editUser.html', context)

@login_required
def dar_de_baja_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    usuario_cargo_unidad = get_object_or_404(UsuarioCargoUnidad, user=user)
    
    if request.method == 'POST':
        user.is_active = False
        user.save()
        usuario_cargo_unidad.estado = False
        usuario_cargo_unidad.save()
        messages.success(request, f'El usuario {user.username} ha sido dado de baja.')
        return redirect('listUser')

    context = {
        'user': user,
        'usuario_cargo_unidad': usuario_cargo_unidad,
    }
    return render(request, 'user/dar_de_baja_confirm.html', context)

@never_cache
@login_required
def list_bitacora(request):
    bitacora_list = Bitacora.objects.all().order_by('-timestamp')
    paginator = Paginator(bitacora_list, 7)  # Cambia 10 al número de registros que deseas por página
    page_number = request.GET.get('page')
    bitacora = paginator.get_page(page_number)
    return render(request, 'user/listBitacora.html', {'bitacora': bitacora})
@login_required
def backup_page(request):
    return render(request, 'user/backup.html')
@login_required
@csrf_exempt
def backup_database(request):
    if request.method == 'POST':
        try:
            # Directorio temporal en el proyecto para crear el archivo
            temp_backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            if not os.path.exists(temp_backup_dir):
                os.makedirs(temp_backup_dir)

            # Nombre del archivo de backup
            date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_backup_file = os.path.join(temp_backup_dir, f'backup_{date_str}.sql')

            # Obtener la ruta de la carpeta de descargas del usuario
            downloads_dir = os.path.join(str(Path.home()), 'Documents')
            final_backup_file = os.path.join(downloads_dir, f'backup_{date_str}.sql')

            # Ruta completa a pg_dump
            pg_dump_path = r'C:\Program Files\PostgreSQL\15\bin\pg_dump.exe'

            if not os.path.exists(pg_dump_path):
                return JsonResponse({'success': False, 'message': f'pg_dump no se encuentra en la ruta especificada: {pg_dump_path}'})

            # Comando para realizar la copia de seguridad
            command = [
                pg_dump_path,
                '-h', settings.DATABASES["default"]["HOST"],
                '-U', settings.DATABASES["default"]["USER"],
                '-d', settings.DATABASES["default"]["NAME"],
                '-f', temp_backup_file
            ]

            # Configurar la variable de entorno PGPASSWORD
            env = os.environ.copy()
            env['PGPASSWORD'] = settings.DATABASES["default"]["PASSWORD"]

            # Ejecutar el comando para crear el archivo de backup
            result = subprocess.run(command, env=env, text=True, capture_output=True)

            # Verificar si hubo errores durante la ejecución del comando
            if result.returncode != 0:
                return JsonResponse({'success': False, 'message': f'Error al ejecutar pg_dump: {result.stderr}'})

            # Mover el archivo a la carpeta de descargas
            shutil.move(temp_backup_file, final_backup_file)

            # Preparar el archivo para descarga
            response = FileResponse(open(final_backup_file, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(final_backup_file)}"'
            return response

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear la copia de seguridad: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def crear_superusuario_view(request):
    # Ejecuta la función para crear el superusuario y captura el resultado
    mensaje = crear_superusuario_y_datos_por_defecto()
    return HttpResponse(mensaje)
@never_cache
@login_required
def listar_secretarias(request):
    # Obtenemos todas las secretarías y prefetchamos las unidades relacionadas
    secretarias = Secretaria.objects.prefetch_related('unidad_set').all()

    return render(request, 'user/listar_secretarias.html', {'secretarias': secretarias})

