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


# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario

    list_display = ('numero_documento','username','tipo','is_staff','is_superuser')
    list_filter  = ('tipo','is_staff','is_superuser','is_active')
    search_fields = ('numero_documento','username','email')
    ordering = ('numero_documento',)

    fieldsets = (
        (None, {'fields': ('numero_documento','username','email','password')}),
        ('Permisos', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Info', {'fields': ('tipo',)}),
        ('Fechas', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_documento','username','email','tipo','password1','password2','is_staff','is_superuser'),
        }),
    )
