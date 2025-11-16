# forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import Usuario, Instructores


class CustomAdminAuthForm(AuthenticationForm):
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


# forms.py
class InstructoresAdminForm(forms.ModelForm):
    # Campos de solo lectura en el admin
    nombres = forms.CharField(required=False, disabled=True)
    numero_documento = forms.CharField(required=False, disabled=True)

    class Meta:
        model = Instructores
        fields = '__all__'
        error_messages = {
            'user': {
                'required': 'Debe seleccionar un usuario de tipo INSTRUCTOR.',
                'unique':   'Este usuario ya está asignado como Instructor.',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Solo usuarios activos tipo INSTRUCTOR
        self.fields['user'].queryset = Usuario.objects.filter(
            is_active=True,
            tipo='INSTRUCTOR'
        )

        instance = getattr(self, 'instance', None)

        # Si estoy EDITANDO un instructor existente
        if instance and instance.pk and instance.user_id:
            user = instance.user
            self.fields['nombres'].initial = user.username
            self.fields['numero_documento'].initial = user.numero_documento

        # Si viene un user desde el POST (después de enviar el form con errores, etc.)
        elif 'user' in self.data:
            user_id = self.data.get('user')
            if user_id:
                try:
                    user = Usuario.objects.get(pk=user_id)
                    self.fields['nombres'].initial = user.username
                    self.fields['numero_documento'].initial = user.numero_documento
                except Usuario.DoesNotExist:
                    pass

    def clean(self):
        cleaned = super().clean()
        user = cleaned.get('user')

        if not user:
            raise ValidationError({'user': 'Debe seleccionar un usuario de tipo INSTRUCTOR.'})
        if getattr(user, 'tipo', None) != 'INSTRUCTOR':
            raise ValidationError({'user': 'El usuario seleccionado no es de tipo INSTRUCTOR.'})
        return cleaned

    def save(self, commit=True):
        """
        Antes de guardar, sincronizamos nombres y número de documento
        con el usuario seleccionado.
        """
        instance = super().save(commit=False)
        if instance.user_id:
            instance.nombres = instance.user.username      # o get_full_name()
            instance.numero_documento = instance.user.numero_documento

        if commit:
            instance.save()
        return instance
    class Media:
        js=("js/instructores_autofill.js")
