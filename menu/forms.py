from django import forms
# from django.forms import (ModelForm, ModelChoiceField, TextInput)
from django.forms import ModelForm
from .models import Alumno, Tutor, Intervencion, Tipo, Novedades, Tarea
# from sysacad.models import Persona
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget
from sysacad.models import Materia
# date picker
from bootstrap_datepicker_plus import DatePickerInput


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
    id = forms.CharField(help_text="Ingrese el legajo o dni del alumno.")

    def clean_id(self):
        data = self.cleaned_data['id']
        if not data.isnumeric():
            raise forms.ValidationError('No ingresó un dni o legajo válido.')
        elif data.isnumeric():
            return data


class agregarAlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = ['dni', 'observaciones']
        # exclude = ['fecha_alta']
        # fields = ['legajo', 'nombre', 'apellido', 'nota', 'comentario', 'fecha_alta']


class agregarIntervencionForm(forms.Form):
    alumno = forms.ModelChoiceField(help_text="Ingrese el alumno involucrado en la intervención.", queryset=Alumno.objects.all(), widget=Select2Widget)
    materia = forms.ModelChoiceField(required=False, help_text="Ingrese la materia a la cual corresponda la consulta.", queryset=Materia.objects.all(), widget=Select2Widget)
    tutor_asignado = forms.ModelChoiceField(help_text="Ingrese el tutor que se encarga de la consulta.", queryset=Tutor.objects.all(), widget=Select2Widget)
    tipo = forms.ModelChoiceField(help_text="Ingrese el tipo de la intervención.", queryset=Tipo.objects.all(), widget=Select2Widget)
    descripcion = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(agregarIntervencionForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['tutor_asignado']


class agregarIntervencionTipoForm(forms.Form):
    descripcion = forms.CharField()

class agregarTutorForm(forms.Form):
    TIPOS = (
        ('Motivacional', 'Motivacional'),
        ('Académico', 'Academico')
    )
    dni = forms.DecimalField(help_text="Ingrese el DNI del tutor.")
    tipo = forms.ChoiceField(choices=TIPOS, help_text="Ingrese el TIPO del tutor.", widget=Select2Widget)
    # tipo = forms.ChoiceField(choices=TIPOS, help_text="Ingrese el TIPO del tutor.")
    horario = forms.CharField(help_text="Ingrese el HORARIO de disponibilidad del tutor.")


class agregarTutorPersonalizadoForm(forms.Form):
    TIPOS = (
        ('Motivacional', 'Motivacional'),
        ('Académico', 'Academico'),
        ('Psicologo', 'Psicologo')
    )
    dni = forms.DecimalField(help_text="Ingrese el DNI del tutor.")
    nombre = forms.CharField(help_text='Ingrese el nombre y apellido completo del nuevo tutor.')
    tipo = forms.ChoiceField(choices=TIPOS, help_text="Ingrese el TIPO del tutor.", widget=Select2Widget)
    telefono = forms.DecimalField(help_text='Ingrese el numero de telefono/celular del tutor.')
    mail = forms.EmailField(help_text='Ingrese el mail del tutor.')
    horario = forms.CharField(help_text="Ingrese el HORARIO de disponibilidad del tutor.")

class buscarTutorForm(forms.Form):
    id = forms.CharField(help_text="Ingrese el legajo o dni del tutor.")

    def clean_id(self):
        data = self.cleaned_data['id']
        # Check dni numerico
        if data.isnumeric():
            return data
        else:
            raise ValidationError('Por favor ingrese un DNI o Legajo valido')

class editarTutorForm(ModelForm):
    class Meta:
        model = Tutor
        exclude = ['']

# class agregarTutorForm(forms.Form):
#     dni = forms.ModelChoiceField(queryset=Persona.objects.none())
#
#     def __init__(self, dni):
#         super(agregarTutorForm, self).__init__()
#         self.fields['dni'].queryset = Persona.objects.filter(numerodocu=dni)

class editarAlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        exclude = ['fecha_desvinculacion']
        widgets = {
            'situacion_riesgo': Select2Widget(choices=(('Si', 'Si'), ('No', 'No')))
        }

class agregarNovedadForm(ModelForm):
    class Meta:
        model = Novedades
        exclude = ['fecha_alta', 'estado']

class editarNovedadForm(ModelForm):
    class Meta:
        model = Novedades
        exclude = ['fecha_alta', 'estado']
#
# class agregarTareaForm(forms.Form):
#     titulo = forms.DecimalField(help_text="Ingrese el titulo de la tarea.")
#     descripcion = forms.CharField(help_text='Ingrese la descripción de la tarea.')
#     fecha_alta = forms.DateTimeField(help_text='Ingrese la fecha de la tarea.')
#     tutor_asignado = forms.ModelChoiceField(help_text="Ingrese el tutor designado de la tarea.", queryset=Tutor.objects.all(), widget=Select2Widget)
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(agregarTareaForm, self).__init__(*args, **kwargs)
#         if not user.is_staff:
#             del self.fields['tutor_asignado']

class agregarTareaForm(ModelForm):
    class Meta:
        model = Tarea
        exclude = ['fecha_baja', 'estado']
        widgets = {
            'fecha_alta': DatePickerInput(format='%Y-%m-%d'),
            'tutor_asignado': Select2Widget
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(agregarTareaForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['tutor_asignado']


class editarTareaForm(ModelForm):
    class Meta:
        model = Tarea
        exclude = ['fecha_baja']
        widgets = {
            'tutor_asignado': Select2Widget,
            'fecha_alta': DatePickerInput(format='%Y-%m-%d'),
        }

class editarIntervencionForm(ModelForm):
    class Meta:
        model = Intervencion
        exclude = ['']
        widgets = {
            'tipo': Select2Widget(choices=Tipo.objects.all()),
            'estado': Select2Widget(choices=(('Abierta', 'Abierta'), ('Cerrada', 'Cerrada'))),
            'fecha_alta': DatePickerInput(format='%Y-%m-%d'),
            'materia': Select2Widget(choices=Materia.objects.all()),
            'tutor_asignado': Select2Widget(choices=Tutor.objects.all()),
            'alumno': Select2Widget(choices=Alumno.objects.all()),
            'fecha_baja': DatePickerInput(format='%Y-%m-%d')

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(editarIntervencionForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['tutor_asignado']
            del self.fields['fecha_baja']
            del self.fields['alumno']
            del self.fields['materia']
            del self.fields['fecha_alta']