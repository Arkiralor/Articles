from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/main/', include('sample_app.endpoints')),
    path('main/', include('sample_app.urls')),

    path('api/user/', include('user_app.endpoints')),
    path('user/', include('user_app.urls'))
]
