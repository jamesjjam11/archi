from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import SystemEvent, get_users_online
from django.db import connection
from django.contrib.auth.models import Group
from django.db.models import Count

@never_cache
@login_required
def monitor_system_view(request):
    # Obtener usuarios conectados en línea
    users_online = get_users_online()
    total_users_online = users_online.count()

    # Obtener cantidad de usuarios por mes
    events_by_month = SystemEvent.objects.annotate(
        month=TruncMonth('timestamp')
    ).values('month').annotate(
        total=Count('id')
    ).order_by('month')

    months = [event['month'].strftime('%Y-%m') for event in events_by_month]
    counts = [event['total'] for event in events_by_month]

    # Obtener los grupos y el número de usuarios en cada grupo
    grupos = Group.objects.annotate(total_users=Count('user')).all()

    # Contar cuántos usuarios están en línea en cada grupo
    grupos_con_usuarios_online = []
    for grupo in grupos:
        users_online_in_group = users_online.filter(groups__name=grupo.name)
        grupos_con_usuarios_online.append({
            'group': grupo,
            'total_users': grupo.total_users,
            'users_online': users_online_in_group.count()
        })

    return render(request, 'monitorSystem.html', {
        'users_online': users_online,
        'total_users_online': total_users_online,
        'months': months,
        'counts': counts,
        'grupos_con_usuarios_online': grupos_con_usuarios_online,
    })


def check_system_availability():
    try:
        # Intenta ejecutar una consulta simple para verificar la conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception as e:
        # Si hay un error, significa que el sistema no está disponible
        return False

@never_cache
@login_required
def system_status_view(request):
    is_system_available = check_system_availability()
    return render(request, 'systemStatus.html', {
        'is_system_available': is_system_available,
    })