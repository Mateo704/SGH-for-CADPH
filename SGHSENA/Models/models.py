from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class Usuario(AbstractUser):
    first_name = None
    last_name = None
    email = None

    numero_documento = models.BigIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1000000000),   # mínimo 10 dígitos
            MaxValueValidator(9999999999),   # máximo 10 dígitos    
        ]
    )

    TIPO_CHOICES = [
        ('SUPERUSER', 'Superusuario'),
        ('COORDINADOR', 'Coordinador'),
        ('INSTRUCTOR', 'Instructor'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='INSTRUCTOR')

    USERNAME_FIELD = 'numero_documento'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.tipo})"

    # 👇 Opcional: sobreescribir permisos para que Django use tu campo tipo
    @property
    def is_staff(self):
        return self.tipo in 'SUPERUSER'

    @property
    def is_superuser(self):
        return self.tipo == 'SUPERUSER'


class Ambientes(models.Model):
    id_ambiente = models.IntegerField(primary_key=True)
    nombre_ambiente = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'ambientes'


class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nombre_perfil = models.CharField(max_length=100)
    descripcion = models.TextField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'perfiles' 


class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'roles'


class Instructores(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    numero_documento = models.BigIntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(1000000000),   # mínimo 10 dígitos
            MaxValueValidator(9999999999),    # máximo 10 dígitos
        ])
    nombres = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, blank=False, null=False)
    id_perfil = models.ForeignKey(Perfiles, models.DO_NOTHING, db_column='id_perfil', blank=False, null=False)
    es_lider = models.BooleanField(default=False)


    class Meta:
        managed = True
        db_table = 'instructores'


class Contratos(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    id_instructor = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor')
    tipo_contrato = models.CharField(max_length=50, blank=False, null=False)
    horas_por_cumplir = models.IntegerField(default=0)
    fecha_inicio = models.DateField(blank=False, null=False)
    fecha_fin = models.DateField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'contratos'


class NivelesFormacion(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    nombre_nivel = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'niveles_formacion'


class ProgramasFormacion(models.Model):
    id_programa = models.AutoField(primary_key=True)
    nombre_programa = models.CharField(max_length=150)
    id_nivel = models.ForeignKey(NivelesFormacion, models.DO_NOTHING, db_column='id_nivel', default=0)
    
    class Meta:
        managed = True
        db_table = 'programas_formacion'


class Jornadas(models.Model):
    Dias_Semana = (
    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miercoles', 'Miércoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sabado', 'Sábado'),
    ('Domingo', 'Domingo'),
    )
    id_jornada = models.AutoField(primary_key=True)
    nombre_jornada = models.CharField(max_length=50)
    hora_inicio = models.TimeField(blank=False, null=False)
    dias_jornada=models.CharField(choices=Dias_Semana, max_length=20, blank=False,null=False)
    hora_fin = models.TimeField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'jornadas'


class Fichas(models.Model):
    id_ficha = models.AutoField(primary_key=True)
    id_programa = models.ForeignKey(ProgramasFormacion, models.DO_NOTHING, db_column='id_programa')
    id_instructor_lider = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor_lider', blank=False, null=False)
    id_ambiente = models.ForeignKey(Ambientes, models.DO_NOTHING, db_column='id_ambiente', blank=False, null=False)
    id_jornada = models.ForeignKey(Jornadas, models.DO_NOTHING, db_column='id_jornada', blank=False, null=False)
    fecha_inicio = models.DateField(blank=False, null=False)
    modalidad = models.CharField(max_length=50, blank=True, null=False)

    class Meta:
        managed = True
        db_table = 'fichas'


class Competencias(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    nombre_competencia = models.CharField(max_length=150)
    programa_relacionado = models.CharField(max_length=100, blank=False, null=False)
    horas = models.IntegerField(default=0)
    id_perfil = models.ForeignKey(Perfiles, models.DO_NOTHING, db_column='id_perfil', blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'competencias'


class ResultadosAprendizaje(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    nombre_resultado = models.CharField(max_length=200)
    id_competencia = models.ForeignKey(Competencias, models.DO_NOTHING, db_column='id_competencia')
    hora_resultado = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'resultados_aprendizaje'


class CompetenciasFichas(models.Model):
    id_comp_ficha = models.AutoField(primary_key=True)
    id_ficha = models.ForeignKey(Fichas, models.DO_NOTHING, db_column='id_ficha')
    id_competencia = models.ForeignKey(Competencias, models.DO_NOTHING, db_column='id_competencia')
    carril = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'competencias_fichas'


class HorasCumplidas(models.Model):
    id_registro = models.AutoField(primary_key=True)
    id_instructor = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor')
    id_ficha = models.ForeignKey(Fichas, models.DO_NOTHING, db_column='id_ficha')
    fecha = models.DateField()
    horas_cumplidas = models.IntegerField(default=0)

    class Meta:
        managed = True
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
        managed = True
        db_table = 'horarios'

class Coordinadores(models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        Nombre=models.CharField(max_length=50, blank=False, null=False)
        numero_documento = models.BigIntegerField(
            null=False,
            blank=False,
            validators=[
            MinValueValidator(1000000000),   # mínimo 10 dígitos
            MaxValueValidator(9999999999),    # máximo 10 dígitos
        ])

        