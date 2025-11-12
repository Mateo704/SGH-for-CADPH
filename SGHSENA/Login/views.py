from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

Usuario = get_user_model()

def login_view(request):
    if request.method == 'POST':
        identificador = request.POST.get('numero_documento')  # puede ser documento o username
        password = request.POST.get('password')

        # Intentar autenticar directamente
        user = authenticate(request, username=identificador, password=password)

        # Si no se encuentra por username, buscar por numero_documento
        if user is None:
            try:
                usuario_obj = Usuario.objects.get(numero_documento=identificador)
                user = authenticate(request, username=usuario_obj.username, password=password)
            except Usuario.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)

            # Redirección según el rol
            if user.is_superuser:
                messages.success(request, f'Bienvenido Administrador {user.username}')
                return redirect('/admin/')

            if user.tipo == 'COORDINADOR':
                messages.success(request, f'Bienvenido Coordinador {user.username}')
                return redirect('dashboard:dashboard_coordinador')

            if user.tipo == 'INSTRUCTOR':
                messages.success(request, f'Bienvenido Instructor {user.username}')
                return redirect('dashboard:dashboard_instructor')

            messages.warning(request, 'Usuario sin rol asignado.')
            return redirect('home')

        messages.error(request, 'Número de documento, nombre de usuario o contraseña incorrectos.')

    return render(request, 'html/login-instructor/login.html')
