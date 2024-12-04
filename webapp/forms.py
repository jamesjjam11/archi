from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Persona, Secretaria, Unidad, Cargo, UsuarioCargoUnidad

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'ci', 'image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }

class SecretariaForm(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = ['nombre_secretaria']

    def clean_nombre_secretaria(self):
        nombre_secretaria = self.cleaned_data['nombre_secretaria']
        if Secretaria.objects.filter(nombre_secretaria=nombre_secretaria).exists():
            raise forms.ValidationError('La Secretaría con este nombre ya existe.')
        return nombre_secretaria

class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['nombre_secretaria', 'nombre_unidad']
    
    def clean_nombre_unidad(self):
        nombre_unidad = self.cleaned_data['nombre_unidad']
        if Unidad.objects.filter(nombre_unidad=nombre_unidad).exists():
            raise forms.ValidationError('La Unidad con este nombre ya existe.')
        return nombre_unidad

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre_cargo']
    
    def clean_nombre_cargo(self):
        nombre_cargo = self.cleaned_data['nombre_cargo']
        if Cargo.objects.filter(nombre_cargo=nombre_cargo).exists():
            raise forms.ValidationError('El Cargo con este nombre ya existe.')
        return nombre_cargo

class UsuarioCargoUnidadForm(forms.ModelForm):
    class Meta:
        model = UsuarioCargoUnidad
        fields = ['nombre_unidad', 'nombre_cargo',]
        widgets = {
            
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'estado': forms.CheckboxInput(),
        }

class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    roles = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Rol')

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'roles')

    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
        'password_too_short': "La contraseña debe tener al menos 8 caracteres.",
        'password_common': "La contraseña no puede ser una contraseña común.",
        'password_entirely_numeric': "La contraseña no puede ser completamente numérica.",
        'password_similar': "La contraseña no puede ser demasiado similar a tu otra información personal.",
        'username_exists': "Este nombre de usuario ya está en uso. Elige otro.",
    }

    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
    )
    email = forms.EmailField(
        label="Correo electrónico",
        max_length=150,
    )
