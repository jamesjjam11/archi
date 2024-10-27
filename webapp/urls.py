from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('crear-superusuario/', views.crear_superusuario_view, name='crear_superusuario'),
    path('login/', views.home, name='login'),
    path('index/', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('listUser/', views.list_user, name='listUser'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('viewUser/<int:user_id>/', views.view_user, name='viewUser'),
    path('editUser/<int:user_id>/', views.edit_user, name='editUser'),
    path('dar_de_baja/<int:user_id>/', views.dar_de_baja_usuario, name='dar_de_baja_usuario'),
    path('bitacora/', views.list_bitacora, name='list_bitacora'),
    path('backup/', views.backup_page, name='backup_page'),
    path('backup/create/', views.backup_database, name='backup_database'), 
    path('listar-secretarias/', views.listar_secretarias, name='listar_secretarias'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)