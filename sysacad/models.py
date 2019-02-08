# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cursos(models.Model):
    curso = models.CharField(max_length=6, primary_key=True)
    anoacademi = models.SmallIntegerField()
    legajo = models.IntegerField(blank=True, null=True)
    facultad = models.SmallIntegerField()
    aula = models.SmallIntegerField(blank=True, null=True)
    horadesde = models.IntegerField(blank=True, null=True)
    horahasta = models.IntegerField(blank=True, null=True)
    especialid = models.SmallIntegerField()
    edificio = models.SmallIntegerField(blank=True, null=True)
    inscriphab = models.CharField(max_length=1, blank=True, null=True)
    tipodictad = models.SmallIntegerField(blank=True, null=True)
    descripcio = models.CharField(max_length=30, blank=True, null=True)
    cupo = models.SmallIntegerField(blank=True, null=True)
    field_oper = models.CharField(db_column='__oper', max_length=1, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_usuario = models.CharField(db_column='__usuario', max_length=12, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_tiempo = models.DateTimeField(db_column='__tiempo', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Sysacad].[Cursos'
        unique_together = (('facultad', 'anoacademi', 'especialid', 'curso'),)


class Materia(models.Model):
    especialid = models.SmallIntegerField()
    plan = models.SmallIntegerField()
    materia = models.SmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=70, blank=True, null=True)
    ano = models.CharField(max_length=1, blank=True, null=True)
    horas = models.SmallIntegerField(blank=True, null=True)
    dictado = models.CharField(max_length=1, blank=True, null=True)
    grupo = models.SmallIntegerField(blank=True, null=True)
    area = models.SmallIntegerField(blank=True, null=True)
    nivel = models.SmallIntegerField(blank=True, null=True)
    llevanota = models.CharField(max_length=1, blank=True, null=True)
    extracurri = models.CharField(max_length=1, blank=True, null=True)
    observacio = models.TextField(blank=True, null=True)  # This field type is a guess.
    creditos = models.SmallIntegerField(blank=True, null=True)
    aprobadote = models.CharField(max_length=1, blank=True, null=True)
    materiadea = models.CharField(max_length=1, blank=True, null=True)
    interna = models.CharField(max_length=1, blank=True, null=True)
    rindelibre = models.CharField(max_length=1, blank=True, null=True)
    asimilacio = models.SmallIntegerField(blank=True, null=True)
    integrador = models.CharField(max_length=1, blank=True, null=True)
    electiva = models.CharField(max_length=1, blank=True, null=True)
    codbloque = models.SmallIntegerField(blank=True, null=True)
    contregobl = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sysacad].[MATERIA'
        unique_together = (('especialid', 'plan', 'materia'),)
        ordering = ['materia']

    def __str__(self):
        return 'Especialidad: {}, Plan: {}, Materia codigo: {}, Nombre: {}'.format(self.especialid, self.plan,
                                                                                   self.materia, self.nombre)


class Matcom(models.Model):
    id = models.IntegerField(primary_key=True)
    facultad = models.SmallIntegerField()
    curso = models.CharField(max_length=6, blank=True, null=True)
    anoacademi = models.SmallIntegerField()
    especialid = models.SmallIntegerField()
    plan = models.SmallIntegerField()
    materia = models.SmallIntegerField()
    comision = models.SmallIntegerField()
    legajo = models.IntegerField(blank=True, null=True)
    aula = models.SmallIntegerField(blank=True, null=True)
    idcomision = models.IntegerField(blank=True, null=True)
    edificio = models.SmallIntegerField(blank=True, null=True)
    parcial = models.SmallIntegerField(blank=True, null=True)
    notaaproba = models.SmallIntegerField(blank=True, null=True)
    notapromoc = models.SmallIntegerField(blank=True, null=True)
    cupo = models.IntegerField(blank=True, null=True)
    dictado = models.CharField(max_length=1, blank=True, null=True)
    año = models.CharField(max_length=1, blank=True, null=True)
    habilitaho = models.CharField(max_length=1, blank=True, null=True)
    titulosnot = models.CharField(max_length=30, blank=True, null=True)
    soloquetra = models.CharField(max_length=1, blank=True, null=True)
    estadoimpn = models.SmallIntegerField(blank=True, null=True)
    idimportac = models.CharField(max_length=9, blank=True, null=True)
    horas = models.SmallIntegerField(blank=True, null=True)
    cuporecurs = models.SmallIntegerField(blank=True, null=True)
    fechapromo = models.DateTimeField(blank=True, null=True)
    cuporefere = models.IntegerField(blank=True, null=True)
    observacio = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_oper = models.CharField(db_column='__oper', max_length=1, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_usuario = models.CharField(db_column='__usuario', max_length=12, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_tiempo = models.DateTimeField(db_column='__tiempo', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Sysacad].[Matcom'
        unique_together = (('facultad', 'anoacademi', 'especialid', 'plan', 'materia', 'comision'),)


class Plan(models.Model):
    especialid = models.SmallIntegerField()
    plan = models.SmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)
    dictadohab = models.CharField(max_length=1, blank=True, null=True)
    asimilado = models.CharField(max_length=1, blank=True, null=True)
    valideztp = models.SmallIntegerField(blank=True, null=True)
    notaap = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sysacad].[PLAN'
        unique_together = (('especialid', 'plan'),)


class Persona(models.Model):
    tipodocume = models.SmallIntegerField()
    numerodocu = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    nombre = models.CharField(max_length=60, blank=True, null=True)
    domicilio = models.CharField(max_length=40, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    piso = models.CharField(max_length=4, blank=True, null=True)
    departamen = models.CharField(max_length=4, blank=True, null=True)
    barrio = models.CharField(max_length=30, blank=True, null=True)
    codigopost = models.SmallIntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fechanacim = models.DateTimeField(blank=True, null=True)
    lugarresid = models.CharField(max_length=60, blank=True, null=True)
    pais = models.SmallIntegerField(blank=True, null=True)
    estadocivi = models.SmallIntegerField(blank=True, null=True)
    nacionalid = models.SmallIntegerField(blank=True, null=True)
    titulosecu = models.SmallIntegerField(blank=True, null=True)
    trabajo = models.CharField(max_length=100, blank=True, null=True)
    direcciont = models.CharField(max_length=30, blank=True, null=True)
    telefonotr = models.CharField(max_length=20, blank=True, null=True)
    horastraba = models.SmallIntegerField(blank=True, null=True)
    escuela = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    resicodigo = models.SmallIntegerField(blank=True, null=True)
    telefonore = models.CharField(max_length=20, blank=True, null=True)
    fechaexpir = models.DateTimeField(blank=True, null=True)
    block = models.CharField(max_length=2, blank=True, null=True)
    mail = models.CharField(max_length=100, blank=True, null=True)
    trabaja = models.CharField(max_length=1, blank=True, null=True)
    tarjeta = models.CharField(max_length=40, blank=True, null=True)
    password = models.CharField(max_length=13, blank=True, null=True)
    localidadn = models.CharField(max_length=30, blank=True, null=True)
    provincian = models.CharField(max_length=30, blank=True, null=True)
    localidad = models.IntegerField(blank=True, null=True)
    sufijocodi = models.CharField(max_length=3, blank=True, null=True)
    modificaci = models.TextField(blank=True, null=True)  # This field type is a guess.
    presentopa = models.CharField(max_length=1, blank=True, null=True)
    certreside = models.CharField(max_length=1, blank=True, null=True)
    certsalud = models.CharField(max_length=1, blank=True, null=True)
    imagen = models.TextField(blank=True, null=True)  # This field type is a guess.
    gruposangu = models.SmallIntegerField(blank=True, null=True)
    imagenes = models.IntegerField(blank=True, null=True)
    universida = models.SmallIntegerField(blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    trabajocen = models.SmallIntegerField(blank=True, null=True)
    tipotrabaj = models.SmallIntegerField(blank=True, null=True)
    ocupación = models.SmallIntegerField(blank=True, null=True)
    cantidadho = models.SmallIntegerField(blank=True, null=True)
    tenenciahi = models.CharField(max_length=1, blank=True, null=True)
    cantidadhi = models.SmallIntegerField(blank=True, null=True)
    cantidadfa = models.SmallIntegerField(blank=True, null=True)
    instrpadre = models.SmallIntegerField(blank=True, null=True)
    situacpadr = models.SmallIntegerField(blank=True, null=True)
    tipopadret = models.SmallIntegerField(blank=True, null=True)
    notrabajap = models.SmallIntegerField(blank=True, null=True)
    ocupacionp = models.SmallIntegerField(blank=True, null=True)
    instrmadre = models.SmallIntegerField(blank=True, null=True)
    situacmadr = models.SmallIntegerField(blank=True, null=True)
    tipomadret = models.SmallIntegerField(blank=True, null=True)
    ocupacionm = models.SmallIntegerField(blank=True, null=True)
    notrabajam = models.SmallIntegerField(blank=True, null=True)
    fechacenso = models.DateTimeField(blank=True, null=True)
    censoproco = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    censoresco = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    cuil = models.CharField(max_length=13, blank=True, null=True)
    telefonomo = models.CharField(max_length=20, blank=True, null=True)
    telefonoem = models.CharField(max_length=20, blank=True, null=True)
    añoegresos = models.SmallIntegerField(blank=True, null=True)
    emipais = models.SmallIntegerField(blank=True, null=True)
    contactoem = models.CharField(max_length=60, blank=True, null=True)
    ndextranje = models.CharField(max_length=16, blank=True, null=True)
    field_oper = models.CharField(db_column='__oper', max_length=1, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_usuario = models.CharField(db_column='__usuario', max_length=12, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_tiempo = models.DateTimeField(db_column='__tiempo', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Sysacad].[Persona'
        unique_together = (('tipodocume', 'numerodocu'),)


class Alumcom(models.Model):
    legajo = models.IntegerField(primary_key=True)
    facultad = models.SmallIntegerField()
    anoacademi = models.SmallIntegerField()
    especialid = models.SmallIntegerField()
    plan = models.SmallIntegerField()
    materia = models.SmallIntegerField()
    comision = models.SmallIntegerField()
    id = models.IntegerField(blank=True, null=True)
    asisestado = models.SmallIntegerField(blank=True, null=True)
    acadestado = models.SmallIntegerField(blank=True, null=True)
    nota1 = models.SmallIntegerField(blank=True, null=True)
    nota2 = models.SmallIntegerField(blank=True, null=True)
    nota3 = models.SmallIntegerField(blank=True, null=True)
    nota4 = models.SmallIntegerField(blank=True, null=True)
    nota5 = models.SmallIntegerField(blank=True, null=True)
    nota6 = models.SmallIntegerField(blank=True, null=True)
    nota7 = models.SmallIntegerField(blank=True, null=True)
    nota8 = models.SmallIntegerField(blank=True, null=True)
    nota9 = models.SmallIntegerField(blank=True, null=True)
    nota10 = models.SmallIntegerField(blank=True, null=True)
    notafinal = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    permitepro = models.CharField(max_length=1, blank=True, null=True)
    numeroequi = models.SmallIntegerField(blank=True, null=True)
    tomo = models.CharField(max_length=6, blank=True, null=True)
    folio = models.SmallIntegerField(blank=True, null=True)
    fecharegul = models.DateTimeField(blank=True, null=True)
    foliadopro = models.CharField(max_length=1, blank=True, null=True)
    anulado = models.CharField(max_length=1, blank=True, null=True)
    tempestado = models.SmallIntegerField(blank=True, null=True)
    origenfacu = models.SmallIntegerField(blank=True, null=True)
    nota11 = models.SmallIntegerField(blank=True, null=True)
    nota12 = models.SmallIntegerField(blank=True, null=True)
    nota13 = models.SmallIntegerField(blank=True, null=True)
    nota14 = models.SmallIntegerField(blank=True, null=True)
    nota15 = models.SmallIntegerField(blank=True, null=True)
    provisorio = models.CharField(max_length=1, blank=True, null=True)
    fechaprovi = models.DateTimeField(blank=True, null=True)
    field_oper = models.CharField(db_column='__oper', max_length=1, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_usuario = models.CharField(db_column='__usuario', max_length=12, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_tiempo = models.DateTimeField(db_column='__tiempo', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    cerrado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sysacad].[alumCom'
        unique_together = (('facultad', 'legajo', 'especialid', 'plan', 'materia', 'comision', 'anoacademi'),)

    def __str__(self):
        return 'Legajo: {}, Facultad: {}, Materia codigo: {}, especialid: {}'.format(self.legajo, self.facultad,
                                                                                   self.materia, self.especialid)


class Alumno(models.Model):
    tipodocume = models.SmallIntegerField(blank=True, null=True)
    numerodocu = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    especialid = models.SmallIntegerField(blank=True, null=True)
    facultad = models.SmallIntegerField()
    legajo = models.IntegerField()
    anoingreso = models.SmallIntegerField(blank=True, null=True)
    plan = models.SmallIntegerField(blank=True, null=True)
    legajoante = models.IntegerField(blank=True, null=True)
    fechaasimi = models.DateTimeField(blank=True, null=True)
    estado = models.SmallIntegerField(blank=True, null=True)
    estudio = models.SmallIntegerField(blank=True, null=True)
    orientacio = models.SmallIntegerField(blank=True, null=True)
    extensiona = models.SmallIntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    tipoingres = models.SmallIntegerField(blank=True, null=True)
    libreta = models.SmallIntegerField(blank=True, null=True)
    excepcion9 = models.CharField(max_length=1, blank=True, null=True)
    observacio = models.TextField(blank=True, null=True)  # This field type is a guess.
    archivoleg = models.CharField(max_length=10, blank=True, null=True)
    documentos = models.IntegerField(blank=True, null=True)
    relacionca = models.SmallIntegerField(blank=True, null=True)
    becacontra = models.CharField(max_length=1, blank=True, null=True)
    becainvest = models.CharField(max_length=1, blank=True, null=True)
    becaeconom = models.CharField(max_length=1, blank=True, null=True)
    becauniver = models.CharField(max_length=1, blank=True, null=True)
    becaintern = models.CharField(max_length=1, blank=True, null=True)
    becanacion = models.CharField(max_length=1, blank=True, null=True)
    becaprovin = models.CharField(max_length=1, blank=True, null=True)
    becamunici = models.CharField(max_length=1, blank=True, null=True)
    becaotro = models.CharField(max_length=1, blank=True, null=True)
    fechaalta = models.DateTimeField(blank=True, null=True)
    reqadminis = models.SmallIntegerField(blank=True, null=True)
    reqacademi = models.SmallIntegerField(blank=True, null=True)
    fechafinin = models.DateTimeField(blank=True, null=True)
    condicione = models.SmallIntegerField(blank=True, null=True)
    turnoprefe = models.CharField(max_length=1, blank=True, null=True)
    turnoalter = models.CharField(max_length=1, blank=True, null=True)
    cue = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tituloante = models.CharField(max_length=100, blank=True, null=True)
    field_oper = models.CharField(db_column='__oper', max_length=1, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_usuario = models.CharField(db_column='__usuario', max_length=12, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_tiempo = models.DateTimeField(db_column='__tiempo', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Sysacad].[alumno'
        unique_together = (('facultad', 'legajo'),)

    def __str__(self):
        return ' DNI: {}'.format(self.numerodocu)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dbo].[django_migrations'


class Especial(models.Model):
    especialid = models.SmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=60, blank=True, null=True)
    abreviatur = models.CharField(max_length=15, blank=True, null=True)
    letra = models.CharField(max_length=1, blank=True, null=True)
    activa = models.CharField(max_length=1, blank=True, null=True)
    tipoespeci = models.SmallIntegerField(blank=True, null=True)
    abrevmail = models.CharField(max_length=12, blank=True, null=True)
    observacio = models.TextField(blank=True, null=True)  # This field type is a guess.
    araufinal = models.IntegerField(blank=True, null=True)
    arauinter = models.IntegerField(blank=True, null=True)
    posgrado = models.CharField(max_length=1, blank=True, null=True)
    sinestadis = models.CharField(max_length=1, blank=True, null=True)
    notaap = models.SmallIntegerField(blank=True, null=True)
    maeespecia = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sysacad].[especial'


class Localidad(models.Model):
    localidad = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=60, blank=True, null=True)
    codigoprov = models.IntegerField(blank=True, null=True)
    field_oper = models.CharField(db_column='__oper', max_length=1, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_usuario = models.CharField(db_column='__usuario', max_length=12, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_tiempo = models.DateTimeField(db_column='__tiempo', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Sysacad].[localidad'


class Paises(models.Model):
    pais = models.SmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    rhun = models.SmallIntegerField(blank=True, null=True)
    araucano = models.SmallIntegerField(blank=True, null=True)
    codsicer = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sysacad].[paises'


class Provincia(models.Model):
    codigoprov = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=60, blank=True, null=True)
    pais = models.SmallIntegerField(blank=True, null=True)
    letraprovi = models.CharField(max_length=1, blank=True, null=True)
    field_oper = models.CharField(db_column='__oper', max_length=1, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_usuario = models.CharField(db_column='__usuario', max_length=12, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_tiempo = models.DateTimeField(db_column='__tiempo', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Sysacad].[provincia'

class Escuela(models.Model):
    escuela = models.DecimalField(max_digits=10, decimal_places=0, primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    codigopost = models.SmallIntegerField(blank=True, null=True)
    domicilio = models.CharField(max_length=40, blank=True, null=True)
    tipoescuel = models.CharField(max_length=1, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    numerodomi = models.CharField(max_length=10, blank=True, null=True)
    field_oper = models.CharField(db_column='__oper', max_length=1, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_usuario = models.CharField(db_column='__usuario', max_length=12, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_tiempo = models.DateTimeField(db_column='__tiempo', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Sysacad].[Escuela'

    def __str__(self):
        return ' Escuela: {}'.format(self.nombre.strip())