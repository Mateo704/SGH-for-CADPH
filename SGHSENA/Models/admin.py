from django.contrib import admin
from .models import (Usuario,
    Instructores, Coordinadores, Ambientes, Competencias,
    CompetenciasFichas, Contratos, Fichas, Horarios,
    HorasCumplidas, Jornadas, NivelesFormacion, Perfiles,
    ProgramasFormacion, ResultadosAprendizaje, Roles
)
# Register your models here.
from django.contrib import admin


admin.site.register(Usuario)
admin.site.register(Coordinadores)
admin.site.register(Ambientes)
admin.site.register(Competencias)
admin.site.register(CompetenciasFichas)
admin.site.register(Contratos)
admin.site.register(Fichas)
admin.site.register(Horarios)
admin.site.register(HorasCumplidas)
admin.site.register(Instructores)
admin.site.register(Jornadas)
admin.site.register(NivelesFormacion)
admin.site.register(Perfiles)
admin.site.register(ProgramasFormacion)
admin.site.register(ResultadosAprendizaje)
admin.site.register(Roles)