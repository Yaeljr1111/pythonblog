from django.http import HttpResponse
from .models import Libro, Autor
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm
from django.contrib.auth.decorators import login_required
from .models import PerfilUsuario
from datetime import date, timedelta
from .models import Prestamo
from django.utils import timezone
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User



@login_required
def dashboard(request):
    total_libros = Libro.objects.count()
    total_autores = Autor.objects.count()
    prestamos_activos = Prestamo.objects.filter(estado='activo').count()
    total_usuarios = User.objects.count()

    return render(request, 'biblioteca/dashboard.html', {
        'total_libros': total_libros,
        'total_autores': total_autores,
        'prestamos_activos': prestamos_activos,
        'total_usuarios': total_usuarios
    })


@login_required
def filtrar_libros(request):
    genero = request.GET.get('genero')
    disponible = request.GET.get('disponible')

    libros = Libro.objects.all()

    if genero:
        libros = libros.filter(genero__iexact=genero)

    if disponible == 'true':
        libros = libros.filter(disponible=True)

    return render(request, 'biblioteca/filtros.html', {
        'libros': libros
    })
@login_required
def busqueda_libros(request):
    query = request.GET.get('q')

    resultados = []

    if query:
        resultados = Libro.objects.filter(
            Q(titulo__icontains=query) |
            Q(autor__nombre__icontains=query)
        )

    return render(request, 'biblioteca/busqueda.html', {
        'resultados': resultados,
        'query': query
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mis_libros_api(request):
    prestamos = Prestamo.objects.filter(usuario=request.user, estado='activo')

    libros = []

    for p in prestamos:
        libros.append({
            'id': p.libro.id,
            'titulo': p.libro.titulo,
            'autor': p.libro.autor.nombre,
            'fecha_prestamo': p.fecha_prestamo,
            'fecha_devolucion': p.fecha_devolucion_esperada
        })

    return Response({'libros': libros})

@api_view(['POST'])
def obtener_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })
    else:
        return Response({'error': 'Credenciales inválidas'}, status=400)

@login_required
def devolver_libro(request, prestamo_id):
    try:
        prestamo = Prestamo.objects.get(id=prestamo_id, usuario=request.user)

        # Marcar como devuelto
        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion_real = timezone.now()
        prestamo.save()

        # Hacer el libro disponible otra vez
        libro = prestamo.libro
        libro.disponible = True
        libro.save()

        return HttpResponse("Libro devuelto correctamente")

    except Prestamo.DoesNotExist:
        return HttpResponse("Préstamo no encontrado")

@login_required
def solicitar_prestamo(request, libro_id):
    try:
        libro = Libro.objects.get(id=libro_id)

        if not libro.disponible:
            return HttpResponse("Libro no disponible")

        # Crear préstamo
        prestamo = Prestamo.objects.create(
            usuario=request.user,
            libro=libro,
            fecha_devolucion_esperada=date.today() + timedelta(days=14)
        )

        # Marcar libro como no disponible
        libro.disponible = False
        libro.save()

        return HttpResponse("Préstamo realizado correctamente")

    except Libro.DoesNotExist:
        return HttpResponse("Libro no encontrado")
    


@login_required
def mis_prestamos(request):
    prestamos = Prestamo.objects.filter(usuario=request.user)
    return render(request, 'biblioteca/mis_prestamos.html', {'prestamos': prestamos})

@login_required
def perfil_usuario(request):
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = PerfilUsuario.objects.create(usuario=request.user)

    html = f"""
    <h1>Perfil de {request.user.username}</h1>
    <p><strong>Nombre:</strong> {request.user.first_name}</p>
    <p><strong>Email:</strong> {request.user.email}</p>
    <p><strong>Teléfono:</strong> {perfil.telefono}</p>
    <p><strong>Dirección:</strong> {perfil.direccion}</p>
    """

    return HttpResponse(html)



@login_required
def inicio(request): 
    html = """ 
    <h1>¡Bienvenido a BiblioTech!</h1> 
    <h2>Tu Biblioteca Digital</h2> 
    <nav> 
        <ul> 
            <li><a href="/libros/">Ver todos los libros</a></li> 
            <li><a href="/autores/">Ver todos los autores</a></li> 
            <li><a href="/libros/genero/ficcion/">Libros de Ficción</a></li> 
            <li><a href="/libros/genero/ciencia/">Libros de Ciencia</a></li> 
        </ul> 
    </nav> 
    """
    if request.user.is_authenticated:
        html += f"<p>Hola {request.user.username} 👋</p>"
        html += '<a href="/perfil/">Ver perfil</a>'
    if request.user.is_authenticated:
        html += '<br><a href="/mis-prestamos/">Ver mis préstamos</a>'

    return HttpResponse(html)

@login_required
def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'biblioteca/libros.html', {'libros': libros})

@login_required
def detalle_libro(request, libro_id):
    try:
        libro = Libro.objects.get(id=libro_id)
        return render(request, 'biblioteca/detalle_libro.html', {'libro': libro})
    except Libro.DoesNotExist:
        return HttpResponse("Libro no encontrado")

@login_required
def lista_autores(request):
    """Vista dinámica de autores"""

    autores = Autor.objects.all()

    html = "<h1>Lista de Autores</h1><ul>"
    for autor in autores:
        html += f"<li>{autor.nombre}</li>"
    html += "</ul>"

    return HttpResponse(html)

@login_required
def detalle_autor(request, autor_id):
    """Vista dinámica de autor"""

    try:
        autor = Autor.objects.get(id=autor_id)

        html = f"<h1>{autor.nombre}</h1><ul>"
        for libro in autor.libros.all():
            html += f"<li>{libro.titulo}</li>"
        html += "</ul>"

        return HttpResponse(html)

    except Autor.DoesNotExist:
        return HttpResponse("Autor no encontrado")

def libros_por_genero(request, genero):
    """Vista que filtra libros por género"""

    generos_disponibles = {
        'ficcion': ['1984', 'El Quijote', 'Cien años de soledad'],
        'ciencia': ['Cosmos', 'Breve historia del tiempo'],
        'historia': ['Sapiens', 'El arte de la guerra']
    }

    if genero in generos_disponibles:
        libros = generos_disponibles[genero]

        html = f"<h1>Libros de {genero.title()}</h1><ul>"
        for libro in libros:
            html += f"<li>{libro}</li>"
        html += "</ul>"
    else:
        html = f"<h1>Género '{genero}' no encontrado</h1>"

    return HttpResponse(html)

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Usuario creado correctamente')
            return redirect('biblioteca:inicio')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'biblioteca/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('biblioteca:inicio')
        else:
            messages.error(request, 'Credenciales incorrectas')

    return render(request, 'biblioteca/login.html')

def logout_usuario(request):
    logout(request)
    return redirect('biblioteca:inicio')

