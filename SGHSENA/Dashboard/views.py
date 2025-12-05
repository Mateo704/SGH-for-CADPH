from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Models.models import (  # asume que en Dashboard.models importas tus modelos o ajusta el import
    Ambientes, Competencias, Fichas, Jornadas,
    Instructores, NivelesFormacion, Horarios
)
from django.views.generic import TemplateView
from django.contrib import messages
from datetime import datetime
from django.db.models import Q

# Palette simple (si quieres agregar colores en la base de datos puedes usar el campo)
PALETTE = [
    "#f87171", "#60a5fa", "#34d399", "#fbbf24", "#a78bfa",
    "#fb7185", "#60a5fa", "#f97316", "#7dd3fc", "#fca5a5"
]


@login_required
def dashboard_instructor(request):
    # Obtener objeto Instructores del user logueado (si existe)
    instructor_obj = None
    try:
        instructor_obj = Instructores.objects.get(user=request.user)
    except Instructores.DoesNotExist:
        instructor_obj = None

    context = {
        "ambientes": Ambientes.objects.all(),
        "competencias": Competencias.objects.all(),
        "fichas": Fichas.objects.all(),
        "jornadas": Jornadas.objects.all(),
        "categoria": NivelesFormacion.objects.all(),
        "instructor_logeado": instructor_obj,
    }
    return render(request, "html/login-instructor/panel_instructor.html", context)


# Endpoint JSON para devolver los horarios filtrados (usado por JS)
@login_required
def horarios_json(request):
    # Instructor obligatorio: el logueado
    try:
        instructor_obj = Instructores.objects.get(user=request.user)
    except Instructores.DoesNotExist:
        return JsonResponse({"error": "Usuario no es instructor"}, status=403)

    qs = Horarios.objects.filter(id_instructor=instructor_obj)

    # Aplicar filtros opcionales (se envían desde el front)
    ambiente = request.GET.get("ambiente")
    competencia = request.GET.get("competencia")
    ficha = request.GET.get("ficha")
    jornada = request.GET.get("jornada")
    fecha = request.GET.get("fecha")  # formato: YYYY-MM-DD

    if ambiente:
        qs = qs.filter(id_ambiente__id_ambiente=ambiente)  # ajuste según FK
    if competencia:
        qs = qs.filter(id_competencia__id_competencia=competencia)
    if ficha:
        qs = qs.filter(id_ficha__id_ficha=ficha)
    if jornada:
        qs = qs.filter(id_jornada__id_jornada=jornada)
    if fecha:
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            qs = qs.filter(fecha=fecha_obj)
        except ValueError:
            pass

    # Armar lista de eventos
    eventos = []
    for h in qs:
        # weekday: Monday=0 ... Sunday=6
        wk = h.fecha.weekday()
        # solo mostramos Lunes(0) .. Sábado(5)
        if wk > 5:
            continue

        comp = h.id_competencia
        comp_name = comp.nombre_competencia if comp else "Sin competencia"
        comp_id = comp.id_competencia if comp else 0

        ambiente_name = h.id_ambiente.nombre_ambiente if h.id_ambiente else ""
        ficha_name = str(h.id_ficha.id_ficha) if h.id_ficha else ""
        jornada_name = h.id_jornada.nombre_jornada if h.id_jornada else ""

        # asignar color determinístico desde palette
        color = PALETTE[comp_id % len(PALETTE)]

        eventos.append({
            "id": h.id_horario,
            "dia_index": wk,  # 0..5 (lunes..sábado)
            "fecha": h.fecha.isoformat(),
            "hora_inicio": h.hora_inicio.strftime("%H:%M"),
            "hora_fin": h.hora_fin.strftime("%H:%M"),
            "competencia": comp_name,
            "competencia_id": comp_id,
            "color": color,
            "ambiente": ambiente_name,
            "ficha": ficha_name,
            "jornada": jornada_name,
        })

    return JsonResponse({"eventos": eventos})

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
