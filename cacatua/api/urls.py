from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # GET
    path('status/', views.get_server_status, name='server_status'),
    path('errors/', views.get_errors, name='all_errors'),
    path('error/<int:code>/', views.get_error_from_code, name='error_detail'),
    
    # POST (Crear)
    path('create/', views.create_error, name='create_error'),
    
    # PUT/DELETE (Actualizar/Borrar) - Usamos el código para identificar cual borrar
    path('update/<int:code>/', views.object_update, name='update_error'),
]