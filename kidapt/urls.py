from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def root_view(request):
    return JsonResponse({'status': 'ok', 'service': 'KidAptitude API', 'message': 'Welcome to the API'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('assessments.urls')),
    path('', include('frontend.urls')),
]
