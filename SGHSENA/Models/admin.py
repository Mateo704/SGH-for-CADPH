# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Usuario, Instructores, Coordinadores, Ambientes, Competencias,
    Contratos, Fichas, Horarios, HorasCumplidas, Jornadas, NivelesFormacion,
    Perfiles, ProgramasFormacion, ResultadosAprendizaje,JornadaDia
)
from .forms import UsuarioCreationForm, UsuarioChangeForm, InstructoresAdminForm
from .forms import CustomAdminAuthForm
from django import forms

admin.site.login_form = CustomAdminAuthForm




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
@admin.register(Instructores)
class InstructoresAdmin(admin.ModelAdmin):
    form = InstructoresAdminForm
    #list_display = ('especialidad', 'es_lider')
    list_display=['es_lider']
    #raw_id_fields = ('id_perfil',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Sólo usuarios activos y de tipo INSTRUCTOR
            kwargs['queryset'] = Usuario.objects.filter(is_active=True, tipo='INSTRUCTOR')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
@admin.register(Coordinadores)
class CoordinadoresAdmin(admin.ModelAdmin):
    #list_display = ('nombre', 'numero_documento', 'user')
    #list_display = ('nombre', 'user')
    list_display = ['user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs["queryset"] = Usuario.objects.filter(
                is_active=True,
                tipo="COORDINADOR"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class JornadaDiaForm(forms.ModelForm):
    class Meta:
        model = JornadaDia
        fields = ['jornada', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir la previsualización de los días seleccionados al formulario
        self.fields['dias_seleccionados'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background-color: #f1f1f1;'}),
            label='Días seleccionados'
        )
        # Actualizar la previsualización cuando el formulario se inicializa
        self.update_previsualizacion()

    def update_previsualizacion(self):
        dias = []
        # Recorrer los días y agregar a la lista si están marcados como True
        if self.instance.Lunes:
            dias.append('Lunes')
        if self.instance.Martes:
            dias.append('Martes')
        if self.instance.Miercoles:
            dias.append('Miércoles')
        if self.instance.Jueves:
            dias.append('Jueves')
        if self.instance.Viernes:
            dias.append('Viernes')
        if self.instance.Sabado:
            dias.append('Sábado')
        if self.instance.Domingo:
            dias.append('Domingo')
        
        # Actualizamos el campo 'dias_seleccionados' con los días seleccionados
        self.fields['dias_seleccionados'].initial = ', '.join(dias) if dias else "Ningún día seleccionado"

@admin.register(JornadaDia)
class JornadaDiaAdmin(admin.ModelAdmin):
    form = JornadaDiaForm
    list_display = ('jornada', 'dias_seleccionados')

    # Definimos el método para acceder a 'dias_seleccionados'
    def dias_seleccionados(self, obj):
        # Llamamos al método del modelo para obtener los días seleccionados
        return obj.dias_seleccionados()  # Llamamos al método 'dias_seleccionados' del modelo
    dias_seleccionados.short_description = "Días seleccionados"  # Opcional: personaliza el nombre en el admin


# Registros simples (¡sin volver a registrar Instructores!)

admin.site.register(Ambientes)
admin.site.register(Competencias)
#admin.site.register(CompetenciasFichas)
admin.site.register(Contratos)
admin.site.register(Fichas)
admin.site.register(Horarios)
admin.site.register(HorasCumplidas)
admin.site.register(Jornadas)
admin.site.register(NivelesFormacion)
admin.site.register(Perfiles)
admin.site.register(ProgramasFormacion)
admin.site.register(ResultadosAprendizaje)

