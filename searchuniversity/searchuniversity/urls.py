from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'Django is running!',
        'debug': settings.DEBUG,
        'database': settings.DATABASES['default']['ENGINE']
    })

urlpatterns = [
    path("", include('base.urls')),
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files explicitly (for environments where staticfiles finder isn't active)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
