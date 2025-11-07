from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.base_user import BaseUserManager
from .managers import UsuarioManager
from django.core.exceptions import ValidationError
from django.conf import settings

# ===============================================================
# USER MANAGER PERSONALIZADO
# ===============================================================
class UsuarioManager(BaseUserManager):

    def create_user(self, numero_documento, password=None, **extra_fields):
        if not numero_documento:
            raise ValueError("El usuario debe tener número de documento")

        user = self.model(numero_documento=numero_documento, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, numero_documento, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo', 'COORDINADOR')  # Opcional

        return self.create_user(numero_documento, password, **extra_fields)


# ===============================================================
# MODELO DE USUARIO PRINCIPAL
# ===============================================================
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from .managers import UsuarioManager  # asumiendo que lo pones aparte

numero_10_digitos = RegexValidator(
    regex=r'^\d{10}$',
    message='El número de documento debe tener exactamente 10 dígitos.'
)

class Usuario(AbstractUser):
    # Quitamos nombres y mantenemos email opcional (útil para admin)
    first_name = None
    last_name = None
    email = models.EmailField(blank=True, null=True)

    # Lo mantenemos pero NO es el login (no único)
    username = models.CharField(max_length=150, blank=False)

    numero_documento = models.BigIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999),
            numero_10_digitos,           # asegura 10 dígitos exactos
        ],
        help_text='Exactamente 10 dígitos.'
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
    REQUIRED_FIELDS = ['username']  # lo pedirá createsuperuser

    # Flags explícitos (AbstractUser ya los trae; si los redefinirás, deja default igual)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    def clean(self):
        super().clean()

        # username obligatorio (aunque no sea login)
        if not self.username or not self.username.strip():
            raise ValidationError({'username': 'El nombre de usuario no puede estar vacío.'})

        # Si es staff, por coherencia pedimos tipo=COORDINADOR
        if self.is_staff and self.tipo not in (None, 'COORDINADOR'):
            raise ValidationError({'tipo': 'Un usuario de staff debe tener tipo "COORDINADOR".'})

        # Si es superuser, forzamos staff y coordinador (coherencia interna)
        if self.is_superuser:
            if not self.is_staff:
                raise ValidationError({'is_staff': 'Un superusuario debe tener is_staff=True.'})
            if self.tipo not in (None, 'COORDINADOR'):
                raise ValidationError({'tipo': 'Un superusuario debe tener tipo "COORDINADOR".'})

    def __str__(self):
        return f"{self.numero_documento} ({self.tipo or 'Sin tipo'})"

    class Meta:
        constraints = [
            # Blindaje en BD: numero_documento de 10 dígitos
            models.CheckConstraint(
                check=Q(numero_documento__gte=1000000000) & Q(numero_documento__lte=9999999999),
                name='usuario_numero_documento_10_digitos_rango'
            ),
            # Si is_superuser => is_staff
            models.CheckConstraint(
                check=Q(is_superuser=False) | Q(is_staff=True),
                name='usuario_superuser_implica_staff'
            ),
            # Si is_staff => tipo es null o COORDINADOR
            models.CheckConstraint(
                check=Q(is_staff=False) | Q(tipo__isnull=True) | Q(tipo='COORDINADOR'),
                name='usuario_staff_tipo_coordinador'
            ),
        ]





class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, numero_documento, password, **extra_fields):
        if not numero_documento:
            raise ValueError("El usuario debe tener número de documento")

        user = self.model(numero_documento=numero_documento, **extra_fields)

        if password is None:
            # Si quieres permitir usuario sin contraseña (no recomendado para superusuario):
            user.set_unusable_password()
        else:
            user.set_password(password)

        # MUY importante para compatibilidad multi-DB:
        user.save(using=self._db)
        return user

    def create_user(self, numero_documento, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(numero_documento, password, **extra_fields)

    def create_superuser(self, numero_documento, password=None, **extra_fields):
        # Fuerza y valida flags
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        if not password:
            # Para superusuario, exige contraseña fuerte
            raise ValueError('El superusuario debe tener una contraseña.')

        # Si quieres marcar tipo por defecto:
        extra_fields.setdefault('tipo', 'COORDINADOR')

        return self._create_user(numero_documento, password, **extra_fields)


# ===============================================================
# TABLA AMBIENTES
# ===============================================================
class Ambientes(models.Model):
    id_ambiente = models.IntegerField(primary_key=True)
    nombre_ambiente = models.CharField(max_length=100)

    class Meta:
        db_table = 'ambientes'


# ===============================================================
# TABLA PERFILES
# ===============================================================
class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nombre_perfil = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'perfiles'


# ===============================================================
# TABLA ROLES
# ===============================================================
class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    class Meta:
        db_table = 'roles'


# ===============================================================
# TABLA INSTRUCTORES
# ===============================================================
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
    numero_documento = models.BigIntegerField(
        validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)]
    )
    nombres = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    id_perfil = models.ForeignKey(Perfiles, models.DO_NOTHING, db_column='id_perfil')
    es_lider = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        # user requerido con mensaje claro
        if not self.user_id:
            raise ValidationError({'user': 'Debe seleccionar un usuario de tipo INSTRUCTOR.'})

        # coherencia: sólo permitir usuarios de tipo INSTRUCTOR
        if getattr(self.user, 'tipo', None) != 'INSTRUCTOR':
            raise ValidationError({'user': 'El usuario seleccionado no es de tipo INSTRUCTOR.'})

    class Meta:
        db_table = 'instructores'
# ===============================================================
# TABLA CONTRATOS
# ===============================================================
class Contratos(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    id_instructor = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor')
    tipo_contrato = models.CharField(max_length=50)
    horas_por_cumplir = models.IntegerField(default=0)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'contratos'


# ===============================================================
# TABLA NIVELES DE FORMACIÓN
# ===============================================================
class NivelesFormacion(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    nombre_nivel = models.CharField(max_length=50)

    class Meta:
        db_table = 'niveles_formacion'


# ===============================================================
# TABLA PROGRAMAS DE FORMACIÓN
# ===============================================================
class ProgramasFormacion(models.Model):
    id_programa = models.AutoField(primary_key=True)
    nombre_programa = models.CharField(max_length=150)
    id_nivel = models.ForeignKey(NivelesFormacion, models.DO_NOTHING, db_column='id_nivel')

    class Meta:
        db_table = 'programas_formacion'


# ===============================================================
# TABLA JORNADAS
# ===============================================================
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
    hora_inicio = models.TimeField()
    dias_jornada = models.CharField(choices=Dias_Semana, max_length=20)
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'jornadas'


# ===============================================================
# TABLA FICHAS
# ===============================================================
class Fichas(models.Model):
    id_ficha = models.AutoField(primary_key=True)
    id_programa = models.ForeignKey(ProgramasFormacion, models.DO_NOTHING, db_column='id_programa')
    id_instructor_lider = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor_lider')
    id_ambiente = models.ForeignKey(Ambientes, models.DO_NOTHING, db_column='id_ambiente')
    id_jornada = models.ForeignKey(Jornadas, models.DO_NOTHING, db_column='id_jornada')
    fecha_inicio = models.DateField()
    modalidad = models.CharField(max_length=50)

    class Meta:
        db_table = 'fichas'


# ===============================================================
# TABLA COMPETENCIAS
# ===============================================================
class Competencias(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    nombre_competencia = models.CharField(max_length=150)
    programa_relacionado = models.CharField(max_length=100)
    horas = models.IntegerField(default=0)
    id_perfil = models.ForeignKey(Perfiles, models.DO_NOTHING, db_column='id_perfil')

    class Meta:
        db_table = 'competencias'


# ===============================================================
# TABLA RESULTADOS DE APRENDIZAJE
# ===============================================================
class ResultadosAprendizaje(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    nombre_resultado = models.CharField(max_length=200)
    id_competencia = models.ForeignKey(Competencias, models.DO_NOTHING, db_column='id_competencia')
    hora_resultado = models.IntegerField(default=0)

    class Meta:
        db_table = 'resultados_aprendizaje'


# ===============================================================
# TABLA COMPETENCIAS - FICHAS
# ===============================================================
class CompetenciasFichas(models.Model):
    id_comp_ficha = models.AutoField(primary_key=True)
    id_ficha = models.ForeignKey(Fichas, models.DO_NOTHING, db_column='id_ficha')
    id_competencia = models.ForeignKey(Competencias, models.DO_NOTHING, db_column='id_competencia')
    carril = models.CharField(max_length=50)

    class Meta:
        db_table = 'competencias_fichas'


# ===============================================================
# TABLA HORAS CUMPLIDAS
# ===============================================================
class HorasCumplidas(models.Model):
    id_registro = models.AutoField(primary_key=True)
    id_instructor = models.ForeignKey(Instructores, models.DO_NOTHING, db_column='id_instructor')
    id_ficha = models.ForeignKey(Fichas, models.DO_NOTHING, db_column='id_ficha')
    fecha = models.DateField()
    horas_cumplidas = models.IntegerField(default=0)

    class Meta:
        db_table = 'horas_cumplidas'


# ===============================================================
# TABLA HORARIOS
# ===============================================================
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


# ===============================================================
# TABLA COORDINADORES
# ===============================================================
class Coordinadores(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    numero_documento = models.BigIntegerField(
        validators=[
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999),
        ]
    )

    class Meta:
        db_table = 'coordinadores'
