from django.urls import path
from . import views

app_name = 'menu'

# el name es el nombre al cual debemos referenciar desde los templates o el codigo html.
urlpatterns = [
    path('', views.index, name = 'index'),
    path('nuevo/', views.agregarAlumno, name = 'nuevo'),
    path('buscar/', views.buscarAlumno, name = 'buscar-alumno'),
    path('nuevo/tutor', views.agregarTutor, name = 'alta-tutor'),
    path('nuevo/tutor-manual', views.agregarTutorPersonalizado, name = 'alta-tutor-personalizada'),
    path('buscar/tutor', views.buscarTutor, name = 'buscar-tutor'),
]
