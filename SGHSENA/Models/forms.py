# forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Instructores
from django.contrib.auth.forms import AuthenticationForm

class CustomAdminAuthForm(AuthenticationForm):
    # Cambia la etiqueta del campo que ve el usuario en /admin/login/
    username = forms.CharField(
        label='# de documento o nombre de usuario',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class UsuarioCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmación de contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('numero_documento', 'username', 'email', 'tipo', 'is_staff', 'is_superuser')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        validate_password(p1, user=None)
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.full_clean()
        if commit:
            user.save()
        return user

class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Contraseña')

    class Meta:
        model = Usuario
        fields = ('numero_documento','username','email','tipo','is_active','is_staff','is_superuser')

    def clean_password(self):
        return self.initial['password']

class InstructoresAdminForm(forms.ModelForm):
    # Los campos a mostrar como solo lectura, no editables
    nombres = forms.CharField(required=False, disabled=True)
    numero_documento = forms.CharField(required=False, disabled=True)

    class Meta:
        model = Instructores
        fields = '__all__'  # Incluye todos los campos del modelo
        error_messages = {
            'user': {
                'required': 'Debe seleccionar un usuario de tipo INSTRUCTOR.',
                'unique':   'Este usuario ya está asignado como Instructor.',
            }
        }

    def __init__(self, *args, **kwargs):
        super(InstructoresAdminForm, self).__init__(*args, **kwargs)
        
        # Si el objeto ya tiene un usuario asociado, rellenamos los campos automáticamente
        if self.instance and self.instance.user:
            self.fields['nombres'].initial = self.instance.user.username  # O usa self.instance.user.get_full_name() si lo tienes
            self.fields['numero_documento'].initial = self.instance.user.numero_documento

        # Si se está creando un nuevo Instructor, se llenarán los campos cuando se seleccione un usuario
        elif 'user' in self.data:
            user_id = self.data.get('user')
            if user_id:
                user = self._meta.model.user.model.objects.get(id=user_id)
                self.fields['nombres'].initial = user.username
                self.fields['numero_documento'].initial = user.numero_documento

    def clean(self):
        cleaned = super().clean()
        user = cleaned.get('user')
        if not user:
            # mensaje claro cuando viene vacío
            raise ValidationError({'user': 'Debe seleccionar un usuario de tipo INSTRUCTOR.'})
        if getattr(user, 'tipo', None) != 'INSTRUCTOR':
            raise ValidationError({'user': 'El usuario seleccionado no es de tipo INSTRUCTOR.'})
        return cleaned