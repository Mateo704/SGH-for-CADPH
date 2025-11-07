from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

Usuario = get_user_model()

'''# ------------------------------------------------------------
# 1️⃣ LOGIN DEL SUPERUSUARIO (solo Django admin)
# ------------------------------------------------------------
#def login_admin_view(request):
    """
    Este login es solo para el superusuario de Django.
    Usa username y password del administrador.
    """
    if request.method == 'POST':
        numero_documento = request.POST.get('numero_documento')
        password = request.POST.get('password')

        user = authenticate(request, numero_documento=numero_documento, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin/')
        else:
            messages.error(request, "Credenciales inválidas o no eres superusuario.")

    return render(request, 'html/login-admin/login.html')


# ------------------------------------------------------------
# 2️⃣ LOGIN GENERAL (Coordinador / Instructor)
# ------------------------------------------------------------
def login_view(request):
    """
    Login personalizado para usuarios con campo numero_documento.
    Redirige según el tipo de usuario (COORDINADOR o INSTRUCTOR).
    """
    if request.method == 'POST':
        numero_documento = request.POST.get('numero_documento')
        password = request.POST.get('password')

        # ✅ Autenticamos directamente con numero_documento
        user = authenticate(request, numero_documento=numero_documento, password=password)

        if user is not None:
            login(request, user)

            # 🔹 Redirección según tipo
            if user.tipo == 'INSTRUCTOR':
                messages.success(request, f'Bienvenido Instructor {user.username}')
                return redirect('dashboard_instructor')

            elif user.tipo == 'COORDINADOR':
                messages.success(request, f'Bienvenido Coordinador {user.username}')
                return redirect('dashboard_coordinador')

            elif user.tipo == 'SUPERUSER':  # En caso de que también lo manejes por tipo
                messages.success(request, f'Bienvenido Administrador {user.username}')
                return redirect('/admin/')

            else:
                messages.warning(request, 'Usuario sin rol asignado.')
                return redirect('home')

        else:
            messages.error(request, 'Número de documento o contraseña incorrectos.')

    return render(request, 'html/login-instructor/login.html')'''

