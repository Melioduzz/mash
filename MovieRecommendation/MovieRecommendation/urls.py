from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r'jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path("", include('Home.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
