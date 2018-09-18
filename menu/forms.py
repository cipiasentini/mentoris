from django import forms
# from django.forms import (ModelForm, ModelChoiceField, TextInput)
from django.forms import ModelForm
from .models import Alumno, Tutor
# from sysacad.models import Persona
from django.core.exceptions import ValidationError


# class ModelTextInput(TextInput):
#     def __init__(self, model_class, query_field, attrs=None):
#         self.model_class = model_class
#         self.query_field = query_field
#         super(ModelTextInput, self).__init__(attrs)
#
#     def render(self, name, value, attrs=None):
#         try:
#             obj = self.model_class.objects.get(pk=value)
#             value = getattr(obj, self.query_field)
#         except:
#             pass
#         return super(ModelTextInput, self).render(name, value, attrs)
#
#     def value_from_datadict(self, data, files, name):
#         try:
#             return self.model_class.objects.get(**{self.query_field: data[name]}).id
#         except:
#             return data[name]
#
#
# class CustomModelChoiceField(ModelChoiceField):
#     def __init__(self, queryset, query_field="pk", **kwargs):
#         if "widget" not in kwargs:
#             kwargs["widget"] = ModelTextInput(model_class=queryset.model, query_field=query_field)
#         super(CustomModelChoiceField, self).__init__(queryset, **kwargs)
#
#     def to_python(self, value):
#         try:
#             int(value)
#         except:
#             from django.core.exceptions import ValidationError
#             raise ValidationError(self.error_messages['invalid_choice'])
#         return super(CustomModelChoiceField, self).to_python(value)


class buscarAlumnoForm(forms.Form):
    legajo_alumno = forms.CharField(help_text="Ingrese el legajo o nombre del alumno.")

    def clean_legajo_alumno(self):
        data = self.cleaned_data['legajo_alumno']

        # Check date is not in past.
        if data.isalpha():
            return data
            # raise ValidationError('El legajo debe ser numerico')
        elif data.isnumeric():
            if (int(data) >= 10000) and (int(data) <= 99999):
                return data
            raise ValidationError('Legajo o nombre invalido')
        else:
            raise ValidationError('Legajo o nombre invalido')


class agregarAlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = ['dni', 'observaciones']
        # exclude = ['fecha_alta']
        # fields = ['legajo', 'nombre', 'apellido', 'nota', 'comentario', 'fecha_alta']


class agregarTutorPersonalizadoForm(ModelForm):
    class Meta:
        model = Tutor
        exclude = ['fecha_alta', 'legajo', 'carrera', 'usuario']

class agregarTutorForm(forms.Form):
    dni = forms.DecimalField(help_text="Ingrese el DNI del tutor.")
    tipo = forms.CharField(help_text="Ingrese el TIPO del tutor.")
    horario = forms.CharField(help_text="Ingrese el HORARIO de disponibilidad del tutor.")
    # usuario = forms.CharField(help_text="Ingrese el USUARIO del tutor.")
    # def clean_dni(self):
    #     data = self.cleaned_data['dni']
    #     # Check dni numerico
    #     if data.isnumeric():
    #         return data
    #     else:
    #         raise ValidationError('Por favor ingrese un DNI valido')


class buscarTutorForm(forms.Form):
    dni = forms.CharField(help_text="Ingrese el DNI del tutor.")
    def clean_dni(self):
        data = self.cleaned_data['dni']
        # Check dni numerico
        if data.isnumeric():
            return data
        else:
            raise ValidationError('Por favor ingrese un DNI valido')


# class agregarTutorForm(forms.Form):
#     dni = forms.ModelChoiceField(queryset=Persona.objects.none())
#
#     def __init__(self, dni):
#         super(agregarTutorForm, self).__init__()
#         self.fields['dni'].queryset = Persona.objects.filter(numerodocu=dni)
