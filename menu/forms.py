from django import forms
from django.forms import ModelForm
from .models import Alumno, Tutor, Intervencion, Tipo, Novedades, Tarea, Grupo, Materia
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget, Select2MultipleWidget
# date picker
from bootstrap_datepicker_plus import DatePickerInput

class buscarAlumnoForm(forms.Form):
    id = forms.ModelChoiceField(help_text="Ingrese el legajo o dni del alumno.", queryset=Alumno.objects.all(), widget=Select2Widget)
    # id = forms.CharField(help_text="Ingrese el legajo o dni del alumno.")

    def clean_id(self):
        data = self.cleaned_data['id']
        if not data.isnumeric():
            raise forms.ValidationError('No ingresó un dni o legajo válido.')
        elif data.isnumeric():
            return data

class agregarAlumnoForm(ModelForm):
    class Meta:
        TIPOS = (
            ('Tecnica', 'Tecnica'),
            ('No tecnica', 'No tecnica')
        )
        model = Alumno
        fields = ['dni', 'ciudad_origen', 'ciudad_residencia', 'tipo_escuela', 'tipo_cursado', 'observaciones',
                  'recursante', 'motivo_recursante', 'discapacidad', 'tipo_discapacidad', 'dejo_seminario',
                  'motivo_dejo_seminario']
        widgets = {
            'tipo_cursado': Select2Widget(choices=(('Libre', 'Libre'), ('Semipresencial', 'Semipresencial'))),
            'tipo_escuela': Select2Widget(choices=TIPOS)
        }
        labels = {
            'tipo_cursado': 'Tipo de cursado del seminario',
            'tipo_escuela': 'Tipo de escuela secundaria'
        }

class agregarIntervencionForm(ModelForm):
    TIPOS = (
        ('Personal', 'Personal'),
        ('Campus virtual', 'Campus virtual'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('Correo electronico', 'Correo electronico'),
        ('Otro', 'Otro')
    )
    alumno = forms.ModelChoiceField(help_text="Ingrese el alumno involucrado en la intervención.",
                                    queryset=Alumno.objects.all(), widget=Select2Widget)
    materia = forms.ModelChoiceField(required=False, help_text="Ingrese la materia a la cual corresponda la consulta.",
                                     queryset=Materia.objects.all(), widget=Select2Widget)
    tutor_asignado = forms.ModelChoiceField(help_text="Ingrese el tutor que se encarga de la consulta.",
                                            queryset=Tutor.objects.all(), widget=Select2Widget)
    tipo = forms.ModelChoiceField(help_text="Ingrese el tipo de la intervención.", queryset=Tipo.objects.all(),
                                  widget=Select2Widget)
    medio = forms.ChoiceField(help_text="Ingrese el medio por el cuál se efectuó la intervención.", choices=TIPOS,
                              widget=Select2Widget)
    descripcion = forms.CharField(widget=forms.Textarea)
    fecha_alta = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))

    def is_valid(self):
        valid = super(agregarIntervencionForm, self).is_valid()
        if not valid:
            for e in super(agregarIntervencionForm, self).errors:
                if e == 'materia':
                    return True
                else:
                    return False
        return valid

    class Meta:
        model = Intervencion
        exclude = ['fecha_baja', 'estado']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(agregarIntervencionForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['tutor_asignado']

class agregarIntervencionTipoForm(ModelForm):
    descripcion = forms.CharField(min_length=4, max_length=40, label='Tipo de intervencion')

    class Meta:
        model = Tipo
        exclude = ['']

# class agregarTutorForm(forms.Form):
#     TIPOS = (
#         ('Motivacional', 'Motivacional'),
#         ('Academico', 'Académico'),
#         ('Psicologo', 'Psicologo'),
#         ('Otro', 'Otro')
#     )
#     dni = forms.DecimalField(help_text="Ingrese el DNI del tutor.")
#     tipo = forms.ChoiceField(choices=TIPOS, help_text="Ingrese el TIPO del tutor.", widget=Select2Widget)
#     # materia = forms.CharField(help_text="Ingrese el materias de las cuales es tutor.")
#     horario = forms.CharField(help_text="Ingrese el HORARIO de disponibilidad del tutor.")

class agregarTutorForm(ModelForm):
    class Meta:
        model = Tutor
        TIPOS = (
            ('Motivacional', 'Motivacional'),
            ('Academico', 'Académico'),
            ('Psicologo', 'Psicologo'),
            ('Otro', 'Otro')
        )
        help_texts = {
            'materia': 'En caso de ser mas de una materia, separarlas con comas'
        }
        fields = ['dni', 'tipo', 'materia', 'horario']
        widgets = {
            'tipo': Select2Widget(choices=TIPOS)
        }

# class agregarTutorPersonalizadoForm(forms.Form):
#     TIPOS = (
#         ('Motivacional', 'Motivacional'),
#         ('Academico', 'Académico'),
#         ('Psicologo', 'Psicologo'),
#         ('Otro', 'Otro')
#     )
#     materia = forms.CharField(help_text="Ingrese el materias de las cuales es tutor.")
#     dni = forms.DecimalField(help_text="Ingrese el DNI del tutor.")
#     nombre = forms.CharField(help_text='Ingrese el nombre y apellido completo del nuevo tutor.')
#     tipo = forms.ChoiceField(choices=TIPOS, help_text="Ingrese el TIPO del tutor.", widget=Select2Widget)
#     telefono = forms.DecimalField(help_text='Ingrese el numero de telefono/celular del tutor.')
#     mail = forms.EmailField(help_text='Ingrese el mail del tutor.')
#     horario = forms.CharField(help_text="Ingrese el HORARIO de disponibilidad del tutor.")

class agregarTutorPersonalizadoForm(ModelForm):
    class Meta:
        model = Tutor
        TIPOS = (
            ('Motivacional', 'Motivacional'),
            ('Academico', 'Académico'),
            ('Psicologo', 'Psicologo'),
            ('Otro', 'Otro')
        )
        fields = ['dni', 'nombre', 'tipo', 'materia', 'telefono', 'mail', 'horario']
        help_texts = {
            'materia': 'En caso de ser mas de una materia, separarlas con comas'
        }
        widgets = {
            'tipo': Select2Widget(choices=TIPOS)
        }

class buscarTutorForm(forms.Form):
    id = forms.ModelChoiceField(help_text="Ingrese el legajo o dni del tutor.", queryset=Tutor.objects.all(), widget=Select2Widget)
    # id = forms.CharField(help_text="Ingrese el legajo o dni del tutor.")

    def __init__(self,*args, **kwargs):
        super(buscarTutorForm, self).__init__(*args, **kwargs)
        self.fields['id'].queryset = self.fields['id'].queryset.order_by('nombre')

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
        exclude = ['fecha_desvinculacion', 'fecha_alta', 'usuario']
        widgets = {
            'tipo': Select2Widget(choices=(('Motivacional', 'Motivacional'),
                                           ('Academico', 'Académico'),
                                           ('Psicologo', 'Psicologo'),
                                           ('Otro', 'Otro'))),
            'fecha_alta': DatePickerInput(format='%Y-%m-%d'),
            'fecha_desvinculacion': DatePickerInput(format='%Y-%m-%d')
        }

class editarAlumnoForm(ModelForm):
    class Meta:
        TIPOS = (
            ('Tecnica', 'Tecnica'),
            ('No tecnica', 'No tecnica')
        )
        model = Alumno
        exclude = ['fecha_desvinculacion', 'fecha_alta']
        widgets = {
            'situacion_riesgo': Select2Widget(choices=(('Si', 'Si'), ('No', 'No'))),
            # 'fecha_alta': DatePickerInput(format='%Y-%m-%d'),
            'tipo_cursado': Select2Widget(choices=(('Libre', 'Libre'), ('Semipresencial', 'Semipresencial'))),
            'tipo_escuela': Select2Widget(choices=TIPOS)
        }

class agregarNovedadForm(ModelForm):
    class Meta:
        model = Novedades
        exclude = ['fecha_alta', 'estado']

class editarNovedadForm(ModelForm):
    class Meta:
        model = Novedades
        exclude = ['fecha_alta', 'estado']

class agregarTareaForm(ModelForm):
    titulo = forms.CharField(help_text='Titulo representativo de la tarea, asi se verá en la agenda de tareas.')
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
            'estado': Select2Widget(choices=(('Abierta', 'Abierta'), ('Cerrada', 'Cerrada'))),
        }

# class editarIntervencionForm(forms.Form):
#     ESTADOS = (
#         ('Abierta', 'Abierta'),
#         ('Cerrada', 'Cerrada')
#     )
#     TIPOS = (
#         ('Personal', 'Personal'),
#         ('Campus virtual', 'Campus virtual'),
#         ('Instagram', 'Instagram'),
#         ('Facebook', 'Facebook'),
#         ('Correo electronico', 'Correo electronico'),
#         ('Otro', 'Otro')
#     )
#     tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(), widget=Select2Widget)
#     estado = forms.ChoiceField(choices=ESTADOS, widget=Select2Widget)
#     descripcion = forms.CharField()
#     fecha_alta = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
#     fecha_baja = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
#     materia = forms.ModelChoiceField(queryset=Materia.objects.all(), widget=Select2Widget)
#     tutor_asignado = forms.ModelChoiceField(queryset=Tutor.objects.all(), widget=Select2Widget)
#     medio = forms.ChoiceField(choices=TIPOS, widget=Select2Widget)
#     alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), widget=Select2Widget)
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(editarIntervencionForm, self).__init__(*args, **kwargs)
#         if not user.is_staff:
#             del self.fields['tutor_asignado']
#             del self.fields['fecha_baja']
#             del self.fields['alumno']
#             del self.fields['materia']
#             del self.fields['fecha_alta']

class editarIntervencionForm(ModelForm):
    ESTADOS = (
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada')
    )
    TIPOS = (
        ('Personal', 'Personal'),
        ('Campus virtual', 'Campus virtual'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('Correo electronico', 'Correo electronico'),
        ('Otro', 'Otro')
    )
    tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(), widget=Select2Widget)
    estado = forms.ChoiceField(choices=ESTADOS, widget=Select2Widget)
    descripcion = forms.CharField(widget=forms.Textarea)
    materia = forms.ModelChoiceField(queryset=Materia.objects.all(), widget=Select2Widget)
    tutor_asignado = forms.ModelChoiceField(queryset=Tutor.objects.all(), widget=Select2Widget)
    medio = forms.ChoiceField(choices=TIPOS, widget=Select2Widget)
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), widget=Select2Widget)
    fecha_alta = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))

    class Meta:
        model = Intervencion
        exclude = ['fecha_baja']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(editarIntervencionForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['tutor_asignado']
            del self.fields['alumno']
            del self.fields['materia']

class agregarGrupoForm(ModelForm):
    ESTADOS = (
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado')
    )
    # estado = forms.ChoiceField(choices=ESTADOS, widget=Select2Widget)
    tutores = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget(), queryset=Tutor.objects.all())
    # alumnos = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget(), queryset=SysacadAlumno.objects.all())
    alumnos = forms.CharField(help_text="Ingrese legajos individualmente seguido de tecla ENTER",
                              widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Ingrese legajos', 'multiple': 'multiple'}))
    titulo = forms.CharField(min_length=4, help_text='Ingrese nombre representativo del grupo, así se lo reconocerá facilmente en las demas pantallas.')
    class Meta:
        model = Grupo
        exclude = ['fecha_baja', 'fecha_alta', 'estado']
        widgets = {
            'fecha_alta': DatePickerInput(format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(agregarGrupoForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['tutores']

class editarGrupoForm(ModelForm):
    ESTADOS = (
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado')
    )
    estado = forms.ChoiceField(choices=ESTADOS, widget=Select2Widget)
    tutores = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget(), queryset=Tutor.objects.all())
    # alumnos = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget(), queryset=Alumno.objects.all())
    alumnos = forms.CharField(help_text="Ingrese legajos individualmente seguido de tecla ENTER",
                              widget=forms.TextInput(
                              attrs={'type': 'text', 'placeholder': 'Ingrese legajos', 'multiple': 'multiple'}))
    titulo = forms.CharField(
        help_text='Ingrese nombre representativo del grupo, así se lo reconocerá facilmente en las demas pantallas.',
        min_length=4)
    class Meta:
        model = Grupo
        exclude = ['fecha_baja']
        widgets = {
            'fecha_alta': DatePickerInput(format='%Y-%m-%d'),
        }

class rankingConsultasTemaForm(forms.Form):
    desde = forms.DateTimeField(widget=DatePickerInput(format='%Y-%m-%d'))
    hasta = forms.DateTimeField(widget=DatePickerInput(format='%Y-%m-%d'))


class agregarEditarMateriaForm(ModelForm):
    TIPOS = (
        ('ISI', 'ISI'),
        ('IQ', 'IQ'),
        ('IEM', 'IEM'),
        ('LAR', 'LAR'),
        ('TCP', 'TCP'),
        ('TUM', 'TUM'),
        ('BASICAS', 'BASICAS')
    )
    materia = forms.CharField(min_length=4, max_length=60, label='Nombre')
    especialidad = forms.ChoiceField(choices=TIPOS, widget=Select2Widget)

    class Meta:
        model = Materia
        exclude = ['']

# class editarIntervencionForm(ModelForm):
#     class Meta:
#         model = Intervencion
#         exclude = ['']
#         widgets = {
#             'tipo': Select2Widget(queryset=Tipo.objects.all()),
#             'estado': Select2Widget(choices=(('Abierta', 'Abierta'), ('Cerrada', 'Cerrada'))),
#             'fecha_alta': DatePickerInput(format='%Y-%m-%d'),
#             'materia': Select2Widget(queryset=Materia.objects.all()),
#             'tutor_asignado': Select2Widget(queryset=Tutor.objects.all()),
#             'alumno': Select2Widget(queryset=Alumno.objects.all()),
#             'fecha_baja': DatePickerInput(format='%Y-%m-%d'),
#         }
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(editarIntervencionForm, self).__init__(*args, **kwargs)
#         if not user.is_staff:
#             del self.fields['tutor_asignado']
#             del self.fields['fecha_baja']
#             del self.fields['alumno']
#             del self.fields['materia']
#             del self.fields['fecha_alta']