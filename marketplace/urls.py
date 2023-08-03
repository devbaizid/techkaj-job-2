
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404
from core.views import custom_404_error


handler404 = custom_404_error




urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path("convert/", include("guest_user.urls")),


]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

