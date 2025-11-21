from django.db import models

from django.db.models import Q
from Models.models import *

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

# Create your models here.
from django.core.exceptions import ValidationError

class Horarios(models.Model):
    id_horario = models.AutoField(primary_key=True)
    id_ficha = models.ForeignKey(Fichas, models.DO_NOTHING, db_column='id_ficha')
    id_instructor = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor')
    id_ambiente = models.ForeignKey(Ambientes, models.DO_NOTHING, db_column='id_ambiente')
    id_jornada = models.ForeignKey(Jornadas, models.DO_NOTHING, db_column='id_jornada')
    id_competencia = models.ForeignKey(Competencias, models.DO_NOTHING, db_column='id_competencia')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'horarios'

    def clean(self):
        super().clean()

        if self.hora_fin <= self.hora_inicio:
            raise ValidationError({'hora_fin': 'La hora fin debe ser mayor que la hora inicio.'})

        # Importar aquí para evitar ciclos si pones la función en otro archivo
        from django.db.models import Q

        qs = Horarios.objects.filter(
            fecha=self.fecha,
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio,
        ).filter(
            Q(id_instructor=self.id_instructor) |
            Q(id_ficha=self.id_ficha) |
            Q(id_ambiente=self.id_ambiente)
        )

        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError('Existe un cruce de horario con otro registro.')

    def __str__(self):
        return f"{self.id_ficha} - {self.id_instructor} - {self.fecha} {self.hora_inicio}-{self.hora_fin}"
