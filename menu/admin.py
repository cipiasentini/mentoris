from django.contrib import admin
from .models import Alumno
from .models import Tutor
from .models import Intervencion, Novedades

admin.site.register(Alumno)
admin.site.register(Tutor)
admin.site.register(Intervencion)
admin.site.register(Novedades)

# con esto yo puedo modificar la manera en que muestro el panel de admin para alumnos
# @admin.register(Alumno)
# class AlumnoAdmin(admin.ModelAdmin):
#     # de la lista cuando entras en alumno
#     list_display = ('legajo', 'apellido', 'nombre')
#
#     # para el formulario de carga
#     # fields = ['legajo', ('nombre', 'apellido')]
#
#     # te lo muestra por secciones
#     fieldsets = (
#         (None, {
#             'fields': ['legajo', ('apellido', 'nombre')]
#         }),
#         ('Notas', {
#             'fields': ('nota', 'comentario', 'fecha_alta')
#         }),
#     )