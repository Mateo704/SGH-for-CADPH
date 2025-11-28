from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render
from Models.models import (
    Ambientes, Competencias, Fichas, Jornadas,
    Instructores, NivelesFormacion
)


def dashboard_instructor(request):

    # Instructor logueado
    instructor = None
    if request.user.is_authenticated:
        try:
            instructor = Instructores.objects.get(user=request.user)
        except Instructores.DoesNotExist:
            
            instructor = None

    context = {
        "ambientes": Ambientes.objects.all(),
        "competencias": Competencias.objects.all(),
        "fichas": Fichas.objects.all(),
        "jornadas": Jornadas.objects.all(),
        "categoria": NivelesFormacion.objects.all(),  # <-- Categorías del programa
        "instructor_logeado": instructor,             # <-- Para fijar instructor en el template
    }

    return render(request, "html/login-instructor/panel_instructor.html", context)


@method_decorator(login_required, name='dispatch')
class DashboardInstructorView(TemplateView):
    template_name = "html/login-instructor/panel_instructor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        instructor = None
        if self.request.user.is_authenticated:
            try:
                instructor = Instructores.objects.get(user=self.request.user)
            except Instructores.DoesNotExist:
                instructor = None

        context["ambientes"] = Ambientes.objects.all()
        context["competencias"] = Competencias.objects.all()
        context["fichas"] = Fichas.objects.all()
        context["jornadas"] = Jornadas.objects.all()
        context["categoria"] = NivelesFormacion.objects.all()
        context["instructor_logeado"] = instructor

        return context

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
