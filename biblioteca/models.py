from django.db import models
from django.contrib.auth.models import User


class Autor(models.Model):
    """Modelo para representar autores de libros"""
    
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=50, blank=True)
    biografia = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Libro(models.Model):
    """Modelo para representar libros"""

    GENEROS = [
        ('ficcion', 'Ficción'),
        ('ciencia', 'Ciencia'),
        ('historia', 'Historia'),
        ('tecnologia', 'Tecnología'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=20, choices=GENEROS, default='ficcion')
    paginas = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor.nombre}"

    def esta_disponible(self):
        return self.disponible

    class Meta:
        ordering = ['-fecha_agregado']


class PerfilUsuario(models.Model):
    """Perfil extendido de usuario"""

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Prestamo(models.Model):
    """Modelo de préstamos"""

    ESTADOS = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"