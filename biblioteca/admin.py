from django.contrib import admin
from .models import Autor, Libro, PerfilUsuario, Prestamo


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nacionalidad', 'fecha_nacimiento']
    search_fields = ['nombre']
    list_filter = ['nacionalidad']


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'genero', 'disponible', 'fecha_publicacion']
    list_filter = ['genero', 'disponible', 'autor']
    search_fields = ['titulo', 'autor__nombre', 'isbn']
    list_editable = ['disponible']


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefono', 'activo']
    list_filter = ['activo']


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion_esperada', 'estado']
    list_filter = ['estado', 'fecha_prestamo']
    search_fields = ['libro__titulo', 'usuario__username']