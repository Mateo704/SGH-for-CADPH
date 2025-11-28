from Models.models import Horarios, Ambientes, Instructores
from django.db.models import Q




def buscar_choques(fecha, hora_inicio, hora_fin, instructor=None, ficha=None, ambiente=None, horario_id=None):
    """
    Devuelve los Horarios que se cruzan con el bloque [hora_inicio, hora_fin)
    para el instructor / ficha / ambiente indicados.
    Si `horario_id` viene, se excluye (útil en updates).
    """
    qs = Horarios.objects.filter(
        fecha=fecha,
        hora_inicio__lt=hora_fin,   # inicio_existente < fin_nuevo
        hora_fin__gt=hora_inicio,   # fin_existente > inicio_nuevo
    )

    condiciones = Q()
    if instructor is not None:
        condiciones |= Q(id_instructor=instructor)
    if ficha is not None:
        condiciones |= Q(id_ficha=ficha)
    if ambiente is not None:
        condiciones |= Q(id_ambiente=ambiente)

    if condiciones:
        qs = qs.filter(condiciones)

    if horario_id is not None:
        qs = qs.exclude(id_horario=horario_id)

    return qs

def horario_instructor_dia(instructor, fecha):
    return Horarios.objects.filter(
        id_instructor=instructor,
        fecha=fecha
    ).select_related('id_ficha', 'id_ambiente', 'id_competencia').order_by('hora_inicio')


def horario_instructor_semana(instructor, fecha_inicio, fecha_fin):
    return Horarios.objects.filter(
        id_instructor=instructor,
        fecha__range=(fecha_inicio, fecha_fin)
    ).select_related('id_ficha', 'id_ambiente', 'id_competencia').order_by('fecha', 'hora_inicio')


def horario_ficha(ficha):
    return Horarios.objects.filter(
        id_ficha=ficha
    ).select_related('id_instructor', 'id_ambiente', 'id_competencia').order_by('fecha', 'hora_inicio')


def horario_por_jornada(jornada):
    return Horarios.objects.filter(
        id_jornada=jornada
    ).select_related('id_ficha', 'id_instructor', 'id_ambiente', 'id_competencia').order_by('fecha', 'hora_inicio')



def ambientes_disponibles(fecha, hora_inicio, hora_fin):
    ocupados = Horarios.objects.filter(
        fecha=fecha,
        hora_inicio__lt=hora_fin,
        hora_fin__gt=hora_inicio,
    ).values_list('id_ambiente_id', flat=True)

    return Ambientes.objects.exclude(id_ambiente__in=ocupados)



def instructores_disponibles(fecha, hora_inicio, hora_fin):
    ocupados = Horarios.objects.filter(
        fecha=fecha,
        hora_inicio__lt=hora_fin,
        hora_fin__gt=hora_inicio,
    ).values_list('id_instructor_id', flat=True)

    return Instructores.objects.exclude(id__in=ocupados)

