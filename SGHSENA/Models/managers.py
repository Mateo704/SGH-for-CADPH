# managers.py

from django.contrib.auth.base_user import BaseUserManager


# ===============================================================
# USER MANAGER PERSONALIZADO
# ===============================================================
class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, numero_documento, password, **extra_fields):
        if not numero_documento:
            raise ValueError("El usuario debe tener número de documento")

        user = self.model(numero_documento=numero_documento, **extra_fields)
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, numero_documento, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(numero_documento, password, **extra_fields)

    def create_superuser(self, numero_documento, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo', 'COORDINADOR')

        if not password:
            raise ValueError('El superusuario debe tener una contraseña.')
        return self._create_user(numero_documento, password, **extra_fields)

