from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages


# 🔹 Vista para instructores
@method_decorator(login_required, name='dispatch')
class DashboardInstructorView(TemplateView):
    template_name = "html/login-instructor/panel_instructor.html"

    def dispatch(self, request, *args, **kwargs):
        # Solo usuarios tipo INSTRUCTOR pueden entrar
        if hasattr(request.user, 'tipo') and request.user.tipo == 'INSTRUCTOR':
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para acceder al panel de instructor.")
        return redirect('login')  # Redirige al login si intenta entrar sin permiso


# 🔹 Vista para coordinadores
@method_decorator(login_required, name='dispatch')
class DashboardCoordinadorView(TemplateView):
    template_name = "html/login-coordinador/panel_coordinador.html"

    def dispatch(self, request, *args, **kwargs):
        # Solo usuarios tipo COORDINADOR pueden entrar
        if hasattr(request.user, 'tipo') and request.user.tipo == 'COORDINADOR':
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No tienes permiso para acceder al panel de coordinador.")
        return redirect('login')
