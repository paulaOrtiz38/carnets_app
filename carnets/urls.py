from django.urls import path
from . import views
from.views import editar_plantilla, generar_pdf_plantilla

urlpatterns = [
    #path('plantilla/<int:pk>/editar/', views.editar_plantilla, name='editar_plantilla'),
    path('plantilla/<int:pk>/editar/', views.editar_plantilla, name='guardar_plantilla'),
    path('plantilla/<int:pk>/orientacion/', views.cambiar_orientacion, name='cambiar_orientacion'),
    path('plantilla/<int:pk>/pdf/', generar_pdf_plantilla, name='generar_pdf'),  # Nueva
    path('api/crear-elemento/', views.crear_elemento, name='crear_elemento'),
    path('api/actualizar-elemento/', views.actualizar_elemento, name='actualizar_elemento'),
    path('api/eliminar-elemento/', views.eliminar_elemento, name='eliminar_elemento'),
]