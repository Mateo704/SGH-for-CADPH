from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.conf import settings
from .managers import UsuarioManager

# ===============================================================
# MODELO DE USUARIO PRINCIPAL
# ===============================================================
numero_7_a_10_digitos = RegexValidator(
    regex=r'^\d{7,10}$',
    message='El número de documento debe tener entre 7 y 10 dígitos.'
)
class Usuario(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(blank=True, null=True)

    username = models.CharField(max_length=150, blank=False)
    numero_documento = models.BigIntegerField(
        'N° de documento',
        unique=True,
        validators=[
            MinValueValidator(1000000),
            MaxValueValidator(9999999999),
            numero_7_a_10_digitos,
        ],
        help_text='De 7 a 10 digitos'
    )

    TIPO_CHOICES = (
        ('COORDINADOR', 'Coordinador'),
        ('INSTRUCTOR', 'Instructor'),
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'numero_documento'
    REQUIRED_FIELDS = ['username']

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    def clean(self):
        super().clean()
        if not self.username or not self.username.strip():
            raise ValidationError({'username': 'El nombre de usuario no puede estar vacío.'})
        if self.is_staff and self.tipo not in (None, 'COORDINADOR'):
            raise ValidationError({'tipo': 'Un usuario de staff debe tener tipo "COORDINADOR".'})
        if self.is_superuser:
            if not self.is_staff:
                raise ValidationError({'is_staff': 'Un superusuario debe tener is_staff=True.'})
            if self.tipo not in (None, 'COORDINADOR'):
                raise ValidationError({'tipo': 'Un superusuario debe tener tipo "COORDINADOR".'})

    def __str__(self):
        return f"{self.username} - {self.numero_documento} ({self.tipo or 'Sin tipo'})"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(numero_documento__gte=1000000) & Q(numero_documento__lte=9999999999),
                name='usuario_numero_documento_7_a_10_digitos_rango'
            ),
            models.CheckConstraint(
                check=Q(is_superuser=False) | Q(is_staff=True),
                name='usuario_superuser_implica_staff'
            ),
            models.CheckConstraint(
                check=Q(is_staff=False) | Q(tipo__isnull=True) | Q(tipo='COORDINADOR'),
                name='usuario_staff_tipo_coordinador'
            ),
        ]

# ===============================================================
# TABLAS RELACIONADAS
# ===============================================================
class Ambientes(models.Model):
    id_ambiente = models.IntegerField(primary_key=True)
    nombre_ambiente = models.CharField(max_length=100)

    class Meta:
        db_table = 'ambientes'

    def __str__(self):
        return self.id_ambiente + " - " + self.nombre_ambiente 

#Perfiles de las competencias
class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nombre_perfil = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'perfiles'

    def __str__(self):
        return self.id_perfil.__str__() + " - " + self.nombre_perfil


class Instructores(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_instructor',
        null=False,
        blank=False,
        error_messages={
            'null':  'Debe seleccionar un usuario de tipo INSTRUCTOR.',
            'blank': 'Debe seleccionar un usuario de tipo INSTRUCTOR.',
            'unique': 'Este usuario ya está asignado como Instructor.',
        }
    )
    profesion = models.CharField(max_length=400)
    es_lider = models.BooleanField(default=False)
    
    def clean(self):
        super().clean()
        if not self.user_id:
            raise ValidationError({'user': 'Debe seleccionar un usuario de tipo INSTRUCTOR.'})
        if getattr(self.user, 'tipo', None) != 'INSTRUCTOR':
            raise ValidationError({'user': 'El usuario seleccionado no es de tipo INSTRUCTOR.'})

    class Meta:
        db_table = 'instructores'

    def __str__(self):
        return self.nombres + " - " + str(self.especialidad)


class Contratos(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    tipo_contrato = models.CharField(max_length=50)
    horas_por_cumplir = models.IntegerField(default=0)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'contratos'

    def __str__(self):
        return f"Contrato {self.id_contrato} - {self.tipo_contrato}"

class NivelesFormacion(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    nombre_nivel = models.CharField(max_length=50)

    class Meta:
        db_table = 'niveles_formacion'

    def __str__(self):
        return self.nombre_nivel


class ProgramasFormacion(models.Model):
    id_programa = models.AutoField(primary_key=True)
    nombre_programa = models.CharField(max_length=150)
    id_nivel = models.ForeignKey(NivelesFormacion, models.DO_NOTHING, db_column='id_nivel')

    class Meta:
        db_table = 'programas_formacion'

    def __str__(self):
        return self.nombre_programa

    def competencias_del_programa(self):
        return self.competencias.filter(es_trasversal=False)

class Jornadas(models.Model):
    id_jornada = models.AutoField(primary_key=True)
    nombre_jornada = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'jornadas'

    def __str__(self):
        return self.nombre_jornada


class JornadaDia(models.Model):

    id = models.AutoField(primary_key=True)
    jornada = models.ForeignKey(
        Jornadas,
        on_delete=models.CASCADE,
        related_name='dias'
    )
    Lunes = models.BooleanField(default=False)
    Martes = models.BooleanField(default=False)
    Miercoles = models.BooleanField(default=False)
    Jueves = models.BooleanField(default=False)
    Viernes = models.BooleanField(default=False)
    Sabado = models.BooleanField(default=False)
    Domingo = models.BooleanField(default=False) 
    class Meta:
        db_table = 'jornadas_dias'

    def __str__(self):
        # Creamos una lista con los días activos
        dias_seleccionados = []
        for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']:
            if getattr(self, dia):  # Si el campo de ese día es True
                dias_seleccionados.append(dia)
        
        # Retornamos el nombre de la jornada y los días seleccionados
        return f"{self.jornada.nombre_jornada} - {', '.join(dias_seleccionados)}" if dias_seleccionados else f"{self.jornada.nombre_jornada} - Ningún día seleccionado"
    
    def dias_seleccionados(self):
        dias = []
        for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']:
            if getattr(self, dia):
                dias.append(dia)
        return ", ".join(dias) if dias else "Ningún día seleccionado"

class Fichas(models.Model):
    Choise_modalidades= (
        ("Presencial", 1),
        ("Virtual", 2),
        ("Hividro", 3),        
    )
    id_ficha = models.IntegerField(primary_key=True)
    id_programa = models.ForeignKey(ProgramasFormacion, models.DO_NOTHING, db_column='id_programa')
    id_instructor_lider = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor_lider')
    id_ambiente = models.ForeignKey(Ambientes, models.DO_NOTHING, db_column='id_ambiente')
    id_jornada = models.ForeignKey(Jornadas, models.DO_NOTHING, db_column='id_jornada')
    fecha_inicio = models.DateField()
    modalidad =  models.CharField(
        max_length=50,
        choices=Choise_modalidades,
        default="Presencial"
    )
    class Meta:
        db_table = 'fichas'

    def __str__(self):
        return f"Ficha {self.id_ficha} - {self.modalidad}"


class Competencias(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    nombre_competencia = models.CharField(max_length=150)
    horas = models.IntegerField(default=0)

    programa_relacionado = models.ForeignKey(
        ProgramasFormacion,
        on_delete=models.CASCADE,
        related_name="competencias",
        null=True,   # permite competencias sin programa
        blank=True   # usadas para transversales
    )

    es_trasversal = models.BooleanField(default=False)

    class Meta:
        db_table = 'competencias'


    def __str__(self):
        return self.nombre_competencia
    

'''class Profesion(models.Model):
    id_profesion = models.AutoField(primary_key=True)
    nombre_profesion = models.CharField(max_length=100)

    # Relación muchos a muchos con Competencias
    competencias = models.ManyToManyField(
        Competencias,
        related_name='profesiones',   # para acceder desde Competencias.prof
        blank=True
    )

    class Meta:
        db_table = 'profesiones'

    def __str__(self):
        return self.nombre_profesion'''



class ResultadosAprendizaje(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    nombre_resultado = models.CharField(max_length=200)
    id_competencia = models.ForeignKey(Competencias, models.DO_NOTHING, db_column='id_competencia')
    hora_resultado = models.IntegerField(default=0)

    class Meta:
        db_table = 'resultados_aprendizaje'

    def __str__(self):
        return self.nombre_resultado


'''class CompetenciasFichas(models.Model):
    id_comp_ficha = models.AutoField(primary_key=True)
    id_competencia = models.ForeignKey(Competencias, models.DO_NOTHING, db_column='id_competencia')
    carril = models.CharField(max_length=50)

    class Meta:
        db_table = 'competencias_fichas'
'''

class HorasCumplidas(models.Model):
    id_registro = models.AutoField(primary_key=True)
    id_instructor = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor')
    id_ficha = models.ForeignKey(Fichas, models.DO_NOTHING, db_column='id_ficha')
    fecha = models.DateField()
    horas_cumplidas = models.IntegerField(default=0)

    class Meta:
        db_table = 'horas_cumplidas'


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


class Coordinadores(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_coordinador',
        null=False,
        blank=False,
        error_messages={
            'null':  'Debe seleccionar un usuario de tipo COORDINADOR.',
            'blank': 'Debe seleccionar un usuario de tipo COORDINADOR.',
            'unique': 'Este usuario ya está asignado como COORDINADOR.',
        }
    )

    class Meta:
        db_table = 'coordinadores'

    def clean(self):
        if self.user.tipo != "COORDINADOR":
            raise ValidationError({
                "user": "El usuario seleccionado debe ser de tipo COORDINADOR."
            })

    def __str__(self):
        return f"{self.user.username} - {self.user.numero_documento}"
 
