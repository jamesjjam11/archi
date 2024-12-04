from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webapp/', include('webapp.urls')),
    path('', RedirectView.as_view(url='/webapp/login/', permanent=True)),
    path('adminapp/', include('adminapp.urls')),
    path('userArchivoapp/', include('userArchivoapp.urls')),
    path('userPersonal/', include('userPersonal.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
