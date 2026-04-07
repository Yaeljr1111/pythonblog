from django.urls import path
from . import views

app_name = 'biblioteca'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autor/<int:autor_id>/', views.detalle_autor, name='detalle_autor'),
    path('libros/genero/<str:genero>/', views.libros_por_genero, name='libros_genero'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('prestamo/<int:libro_id>/', views.solicitar_prestamo, name='prestamo'),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('devolver/<int:prestamo_id>/', views.devolver_libro, name='devolver'),
    path('api/token/', views.obtener_token, name='api_token'),
    path('api/mis-libros/', views.mis_libros_api, name='api_mis_libros'),
    path('buscar/', views.busqueda_libros, name='buscar'),
    path('filtros/', views.filtrar_libros, name='filtros'),
    path('dashboard/', views.dashboard, name='dashboard'),
]