from django.db import models
from django.utils import timezone
# from compositefk.fields import CompositeForeignKey

class Persona(models.Model):
    dni = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    nombre = models.CharField(max_length=60, blank=True)
    # telefono = models.CharField(max_length=20, blank=True, null=True)
    # mail = models.CharField(max_length=100, blank=True, null=True)
    # carrera = models.CharField(max_length=20, blank=True, null=True)
    # fecha_alta = models.DateTimeField(default=timezone.now)
    # dni = models.OneToOneField('sysacad.Persona', verbose_name='DNI', primary_key=True, on_delete=models.DO_NOTHING)
    # dni = models.ForeignKey('sysacad.Persona', verbose_name='DNI', on_delete=models.DO_NOTHING)
    legajo = models.IntegerField(unique=True, blank=True, null=True)
    fecha_alta = models.DateTimeField(default=timezone.now)
    fecha_desvinculacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class Tutor(Persona):
    # legajo = models.IntegerField(unique=True, blank=True, null=True)
    tipo = models.CharField(max_length=30)
    horario = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.CharField(max_length=20, blank=True, null=True)
    # fecha_desvinculacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return ' Nombre de tutor: {}, Tipo: {}'.format(self.nombre, self.tipo)

class Alumno(Persona):
    # legajo = models.IntegerField(unique=True, blank=True)
    situacion_riesgo = models.CharField(max_length=60, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return ' Legajo: {}, Nombre: {}'.format(self.legajo, self.nombre)


class Intervencion(models.Model):
    tipo = models.CharField(max_length=40, null=True, blank=True)
    estado = models.CharField(max_length=40, default='Abierta')
    descripcion = models.TextField(null=True, blank=True)
    fecha_alta = models.DateTimeField(default=timezone.now)
    fecha_baja = models.DateTimeField(null=True, blank=True)
    # especialid = models.ForeignKey('sysacad.Materia', on_delete=models.DO_NOTHING)
    # plan = models.ForeignKey('sysacad.Materia', on_delete=models.DO_NOTHING)
    materia = models.ForeignKey('sysacad.Materia', on_delete=models.DO_NOTHING)
    tutor_asignado = models.ForeignKey('Tutor', on_delete=models.DO_NOTHING)
    alumno = models.ForeignKey('Alumno', on_delete=models.DO_NOTHING)

    # dni = CompositeForeignKey('sysacad.Materia', on_delete=models.DO_NOTHING, related_name=persona, to_fields={
    #     "tipodocume":
    # })
    # class Meta:
    #     app_label = 'menu'