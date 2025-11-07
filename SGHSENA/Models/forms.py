# forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from .models import Usuario

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
