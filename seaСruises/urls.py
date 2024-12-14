from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),
    path('', include('myapp.urls')),
    # path('cruise/', cruise_details, name='cruise'),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
