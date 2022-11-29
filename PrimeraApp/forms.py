from django.forms import ModelForm
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Experiencias, Cursos, Profile_Experiencias, Formulario


class Form_Experiencia(ModelForm):
    class Meta:
        model = Experiencias
        fields = ["evaluacion", "mensaje"]
        widgets = {
                'mensaje': forms.Textarea(attrs={'cols': 100, 'rows': 20}),
            }
                

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



    
class SearchForm(forms.Form):
    name = forms.CharField(max_length=25)

    
        
class SettingsForm(forms.Form):
    lista = ( ("Experiencias", 'Experiencias'),("Users", 'Users'), ("Cursos", 'Cursos'))

    seccion = forms.ChoiceField(choices=lista)


class CursosForm(ModelForm):
    class Meta:
        model = Cursos
        fields = ["título", "subtítulo", "cuerpo", "imagen"]
        enctype="multipart/form-data"

class Profile_ExperienciasForm(ModelForm):
    class Meta:
        model = Profile_Experiencias
        fields = ["experiencia", "usuario"]

class FormularioForm(ModelForm):
    class Meta:
        model = Formulario
        fields = ["nombre", "apellido", "curso", "mail", "celular"]

