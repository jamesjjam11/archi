from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('monitor/', views.monitor_system_view, name='monitor_system'),
    path('monitor/system-status/', views.system_status_view, name='system_status'),
]