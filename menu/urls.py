from django.urls import path
from . import views

app_name = 'menu'

# el name es el nombre al cual debemos referenciar desde los templates o el codigo html.
urlpatterns = [
    path('', views.index, name = 'index'),
    path('nuevo/alumno', views.agregarAlumno, name = 'alta-alumno'),
    path('editar/alumno/<int:dni>/', views.editarAlumno, name='editar-alumno'),
    path('buscar/alumno', views.buscarAlumno, name = 'buscar-alumno'),
    path('nuevo/tutor', views.agregarTutor, name = 'alta-tutor'),
    path('nuevo/tutor-manual', views.agregarTutorPersonalizado, name = 'alta-tutor-personalizada'),
    path('buscar/tutor', views.buscarTutor, name = 'buscar-tutor'),
    path('nueva/intervencion', views.agregarIntervencion, name = 'alta-intervencion'),
    path('nueva/intervencion/tipo', views.agregarIntervencionTipo, name = 'alta-tipo-intervencion'),
    path('intervenciones', views.listarIntervenciones, name = 'intervenciones'),
    path('intervenciones/cerrar/<int:id>/', views.cerrarIntervencion, name = 'cerrar-intervencion'),
    path('intervenciones/abrir/<int:id>/', views.abrirIntervencion, name = 'abrir-intervencion'),
]
