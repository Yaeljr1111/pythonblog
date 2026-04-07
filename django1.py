# crear entorno y preparacion

# cd ruta de la carpeta / arrastrar carpeta a warp
# crear entorno virtual - python -m venv venv
# activar - venv\Scripts\activate


# Ejercicios Prácticos: Guía de Ejercicios: Django Framework
# Ejercicio 1: Configuración Inicial del Proyecto Biblioteca Digital 


# Paso 1: Instalación de Django Instala Django en tu entorno de desarrollo.
# pip install django


# Paso 2: Crear el proyecto principal Crea un proyecto Django llamado “bibliotech_project”.
# django-admin startproject bibliotech_project
# entrar al proyecto - cd bibliotech_project

# Paso 3: Explorar la estructura creada Examina los archivos generados y completa la descripción de cada uno:

# Paso 4: Crear la aplicación “biblioteca” Dentro del proyecto, crea una aplicación llamada “biblioteca”.
# python manage.py startapp

# todo esto hasta aqui en terminal

# Paso 5: Registrar la aplicación Abre el archivo settings.py y registra la aplicación “biblioteca” en INSTALLED_APPS.
"""
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'biblioteca',
]"""


# Paso 6: Configuración inicial de la base de datos Ejecuta las migraciones iniciales para configurar la base de datos.

# python manage.py migrate

# Paso 7: Crear un superusuario Crea un superusuario para acceder al panel de administración. - pendiente

# Paso 8: Verificar la instalación Inicia el servidor de desarrollo y verifica que todo funcione correctamente. ejecutar en warp



# Ejercicio 2: Sistema de URLs y Vistas Básicas 
#Paso 1: Crear el archivo URLs de la aplicación En la carpeta “biblioteca”, crea un archivo urls.py. 
# biblioteca/urls.py 
"""
from django.urls import path 
from . import views 
# Define el namespace de la aplicación 
app_name = 'biblioteca' 
urlpatterns = [ 
# Completa las rutas aquí 
path('', views.______, name='inicio'), 
path('libros/', views.______, name='lista_libros'), 
path('libro/<int:libro_id>/', views.______, name='detalle_libro'), 
path('autores/', views.______, name='lista_autores'), 
path('autor/<int:autor_id>/', views.______, name='detalle_autor'), 
]
"""







