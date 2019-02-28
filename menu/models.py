from django.db import models
from django.utils import timezone
# from compositefk.fields import CompositeForeignKey

class Tipo(models.Model):
    descripcion = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        for campo in ['descripcion']:
            val = getattr(self, campo, False)
            if val:
                val = val.rstrip().replace(',', '').split()
                valor = ''
                for i in val:
                    valor += i.lower().capitalize()+' '
                valor = valor.rstrip()
                setattr(self, campo, valor)
        super(Tipo, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.descripcion)

class Persona(models.Model):
    dni = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    nombre = models.CharField(max_length=60)
    telefono = models.BigIntegerField(blank=True, null=True)
    mail = models.EmailField(max_length=100)
    # carrera = models.CharField(max_length=20, blank=True, null=True)
    # fecha_alta = models.DateTimeField(default=timezone.now)
    # dni = models.OneToOneField('sysacad.Persona', verbose_name='DNI', primary_key=True, on_delete=models.DO_NOTHING)
    # dni = models.ForeignKey('sysacad.Persona', verbose_name='DNI', on_delete=models.DO_NOTHING)
    # legajo = models.IntegerField(unique=True, blank=True, null=True)
    fecha_alta = models.DateTimeField(default=timezone.now)
    fecha_desvinculacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class Tutor(Persona):
    # legajo = models.IntegerField(unique=True, blank=True, null=True)
    legajo = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=30)
    materia = models.CharField(max_length=100, blank=True, null=True)
    horario = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.CharField(max_length=20, blank=True, null=True)
    # fecha_desvinculacion = models.DateTimeField(null=True, blank=True)

    def estado(self):
        if self.fecha_desvinculacion:
            return 'Inactivo'
        else:
            return 'Activo'

    def save(self, *args, **kwargs):
        for campo in ['nombre', 'materia']:
            val = getattr(self, campo, False)
            if val:
                val = val.rstrip().replace(',', '').split()
                valor = ''
                for i in val:
                    valor += i.lower().capitalize()+' '
                valor = valor.rstrip()
                setattr(self, campo, valor)
        super(Tutor, self).save(*args, **kwargs)

    def __str__(self):
        return 'DNI: {}; Nombre: {}; Tipo: {} --- Estado: {}'.format(self.dni, self.nombre, self.tipo, self.estado())

class Alumno(Persona):
    ciudad_origen = models.CharField(max_length=60, null=True, blank=True)
    ciudad_residencia = models.CharField(max_length=60, null=True, blank=True)
    tipo_escuela = models.CharField(max_length=20, null=True, blank=True, default='No tecnica')
    legajo = models.IntegerField(unique=True)
    situacion_riesgo = models.CharField(max_length=60, null=True, blank=True, default='No')
    tipo_cursado = models.CharField(max_length=60, null=True, blank=True, default='Semipresencial')
    recursante = models.BooleanField(default=False, blank=True)
    motivo_recursante = models.CharField(max_length=60, null=True, blank=True, default=None)
    discapacidad = models.BooleanField(default=False)
    tipo_discapacidad = models.CharField(max_length=40, null=True, blank=True, default=None)
    dejo_seminario = models.BooleanField(default=False, blank=True)
    motivo_dejo_seminario = models.CharField(max_length=60, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        for campo in ['nombre', 'ciudad_origen', 'ciudad_residencia', 'motivo_recursante', 'motivo_dejo_seminario', 'tipo_discapacidad']:
            val = getattr(self, campo, False)
            if val:
                val = val.rstrip().replace(',', '').split()
                valor = ''
                for i in val:
                    valor += i.lower().capitalize()+' '
                valor = valor.rstrip()
                setattr(self, campo, valor)
        setattr(self, 'observaciones', getattr(self, 'observaciones', False).capitalize())
        super(Persona, self).save(*args, **kwargs)

    def __str__(self):
        return ' Legajo: {}, DNI: {}, Nombre: {}'.format(self.legajo, self.dni, self.nombre)

class Intervencion(models.Model):
    alumno = models.ForeignKey('Alumno', on_delete=models.DO_NOTHING)
    materia = models.ForeignKey('sysacad.Materia', on_delete=models.DO_NOTHING, null=True, blank=True)
    tutor_asignado = models.ForeignKey('Tutor', on_delete=models.DO_NOTHING)
    tipo = models.ForeignKey('Tipo', on_delete=models.DO_NOTHING)
    medio = models.CharField(max_length=40, default='Personal')
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=40, default='Abierta')
    fecha_alta = models.DateTimeField(default=timezone.now)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        setattr(self, 'descripcion', getattr(self, 'descripcion', False).capitalize())
        super(Intervencion, self).save(*args, **kwargs)

    def __str__(self):
        return 'Alumno: {}, Intervencion: {}, {}'.format(self.alumno, self.tipo, self.descripcion)

class Novedades(models.Model):
    titulo = models.CharField(max_length=60, null=True, blank=True)
    descripcion = models.TextField()
    fecha_alta = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=40, default='Activa')

    def save(self, *args, **kwargs):
        for campo in ['titulo']:
            val = getattr(self, campo, False)
            if val:
                val = val.rstrip().replace(',', '').split()
                valor = ''
                for i in val:
                    valor += i.lower().capitalize()+' '
                valor = valor.rstrip()
                setattr(self, campo, valor)
        setattr(self, 'descripcion', getattr(self, 'descripcion', False).capitalize())
        super(Novedades, self).save(*args, **kwargs)

class Tarea(models.Model):
    titulo = models.CharField(max_length=60, null=True, blank=True)
    descripcion = models.TextField()
    fecha_alta = models.DateTimeField(default=timezone.now, verbose_name='Fecha programada')
    fecha_baja = models.DateTimeField(null=True, blank=True)
    tutor_asignado = models.ForeignKey('Tutor', on_delete=models.DO_NOTHING)
    estado = models.CharField(max_length=40, default='Abierta')

    def get_absolute_url(self):
        return "/tarea/%d" % self.id

    def save(self, *args, **kwargs):
        for campo in ['titulo']:
            val = getattr(self, campo, False)
            if val:
                val = val.rstrip().replace(',', '').split()
                valor = ''
                for i in val:
                    valor += i.lower().capitalize()+' '
                valor = valor.rstrip()
                setattr(self, campo, valor)
        setattr(self, 'descripcion', getattr(self, 'descripcion', False).capitalize())
        super(Tarea, self).save(*args, **kwargs)

class Grupo(models.Model):
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField(null=True, blank=True)
    fecha_alta = models.DateTimeField(default=timezone.now)
    fecha_baja = models.DateTimeField(null=True, blank=True)
    horario = models.CharField(max_length=50, blank=True, null=True)
    alumnos = models.ManyToManyField(Alumno)
    tutores = models.ManyToManyField(Tutor)
    estado = models.CharField(max_length=20, null=True, blank=True, default='Abierto')

    def __str__(self):
        return ' Grupo: {}, Horario: {}'.format(self.titulo, self.horario)

    def save(self, *args, **kwargs):
        for campo in ['titulo']:
            val = getattr(self, campo, False)
            if val:
                val = val.rstrip().replace(',', '').split()
                valor = ''
                for i in val:
                    valor += i.lower().capitalize()+' '
                valor = valor.rstrip()
                setattr(self, campo, valor)
        setattr(self, 'descripcion', getattr(self, 'descripcion', False).capitalize())
        super(Grupo, self).save(*args, **kwargs)