from django.contrib.auth.models import User, Group, Permission
from django.db.utils import IntegrityError
from webapp.models import Persona, Secretaria, Unidad, Cargo, UsuarioCargoUnidad

def crear_grupos_y_permisos():
    # Definir los nombres de los grupos y sus permisos
    grupos_y_permisos = {
        'SuperAdmin': Permission.objects.all(),  # Todos los permisos
        'Admin': Permission.objects.filter(codename__in=['add_user', 'change_user', 'delete_user', 'view_user']),
        'userArchivo': Permission.objects.filter(codename__in=['add_document', 'change_document', 'view_document']),
        'userPersonal': Permission.objects.filter(codename__in=['add_persona', 'change_persona', 'view_persona']),
    }

    for grupo_nombre, permisos in grupos_y_permisos.items():
        group, created = Group.objects.get_or_create(name=grupo_nombre)
        if created:
            group.permissions.set(permisos)
            print(f'Grupo {grupo_nombre} creado con sus permisos.')
        else:
            print(f'Grupo {grupo_nombre} ya existente.')

def crear_superusuario_y_datos_por_defecto():
    try:
        # Verifica si existe un superusuario
        if not User.objects.filter(is_superuser=True).exists():
            print('No existe un superusuario. Procediendo a crear uno.')
            
            # Crea el superusuario
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Hola123-'
            )
            print('Superusuario creado.')

            # Crea una Persona asociada al superusuario
            persona = Persona.objects.create(
                user=user,
                nombre='Admin',
                apellido_paterno='Super',
                apellido_materno='User',
                ci='12345678'
            )
            print('Persona asociada al superusuario.')

            # Verifica si ya existe una secretaría por defecto
            secretaria, created_secretaria = Secretaria.objects.get_or_create(
                nombre_secretaria='SECRETARIA DEP. ADMINISTRATIVA FINANCIERA'
            )
            if created_secretaria:
                print('Secretaría por defecto creada.')
            else:
                print('Secretaría por defecto ya existente.')

            # Verifica si ya existe una unidad por defecto
            unidad, created_unidad = Unidad.objects.get_or_create(
                nombre_secretaria=secretaria,  # Relación con la secretaría
                nombre_unidad='SISTEMAS UF'
            )
            if created_unidad:
                print('Unidad por defecto creada.')
            else:
                print('Unidad por defecto ya existente.')

            # Crea un Cargo por defecto
            cargo, created_cargo = Cargo.objects.get_or_create(
                nombre_cargo='SuperAdmin'
            )
            if created_cargo:
                print('Cargo por defecto creado.')
            else:
                print('Cargo por defecto ya existente.')

            # Asocia la unidad y el cargo al usuario
            UsuarioCargoUnidad.objects.create(
                user=user,
                nombre_unidad=unidad,
                nombre_cargo=cargo
            )
            print('Información adicional creada y asociada.')

            # Crear grupos y permisos
            crear_grupos_y_permisos()  # Asegúrate de que esta línea se esté ejecutando

            # Asignar el usuario al grupo superAdmin
            group_superadmin = Group.objects.get(name='SuperAdmin')
            user.groups.add(group_superadmin)
            print('Superusuario agregado al grupo SuperAdmin.')

            return 'Superusuario, roles y datos por defecto creados con éxito.'

        else:
            print('Ya existe un superusuario.')
            return 'Ya existe un superusuario.'

    except IntegrityError as e:
        print(f"Error de integridad: {e}")
        return f"Error de integridad: {e}"

    except Exception as e:
        print(f"Error inesperado: {e}")
        return f"Error inesperado: {e}"
