# <tu_app>/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class DocumentoOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        if username is None:
            return None

        user = None
        # Intentar como documento
        try:
            user = User.objects.get(numero_documento=username)
        except (User.DoesNotExist, ValueError):
            # Si no es un número de 10 dígitos, intentar como username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
