from django.db import models
from django.utils import timezone

class Persona(models.Model):
    dni = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    nombre = models.CharField(max_length=60, blank=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    mail = models.CharField(max_length=100, blank=True, null=True)
    carrera = models.CharField(max_length=20, blank=True, null=True)
    fecha_alta = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class Tutor(Persona):
    legajo = models.IntegerField(unique=True, blank=True, null=True)
    tipo = models.CharField(max_length=30)
    horario = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.CharField(max_length=20, null=True)

    def __str__(self):
        return ' Nombre de tutor: {}, Tipo: {}'.format(self.nombre, self.tipo)

class Alumno(Persona):
    legajo = models.IntegerField(unique=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return ' Legajo: {}, Nombre: {}'.format(self.legajo, self.nombre)

class Intervencion(models.Model):
    tipo = models.TextField(max_length=40, null=True, blank=True)
    estado = models.TextField(max_length=40, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_alta = models.DateTimeField(default=timezone.now)
    materia = models.TextField(max_length=40, null=True, blank=True)
    tutor_asignado = models.ForeignKey('Tutor', on_delete=models.DO_NOTHING)