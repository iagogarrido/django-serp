from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from serp.validators import validate_bic, validate_iban, validate_nif, validate_codpostal

# Create your models here.

TIPO_COBRO = (
    ('I', 'Ingreso'),
    ('G', 'Gasto'),
)

TIPO_PRESENTADOR = (
    ('PF', 'Persona física'),
    ('PJ', 'Persona juridica'),
)

PERIODICIDAD = (
    (1, 'Mensual'),
    (3, 'Trimestral'),
    (4, 'Cuatrimestral'),
    (6, 'Semestral'),
    (12, 'Anual'),
)


class Cliente(models.Model):
    referencia = models.CharField(max_length=35)
    nombre = models.CharField(max_length=70)
    nif = models.CharField(max_length=35, validators=[validate_nif])
    direccion = models.CharField(max_length=140)
    codpostal = models.CharField("cod. postal", max_length=10, validators=[validate_codpostal])
    poblacion = models.CharField(max_length=90)
    provincia = models.CharField(max_length=50)
    email = models.CharField(max_length=256, validators=[validate_email])
    bic = models.CharField("codigo BIC", max_length=11, validators=[validate_bic])
    iban = models.CharField("numero IBAN", max_length=34, validators=[validate_iban])

    def get_absolute_url(self):
        return reverse('serp:persona-update', args=(self.pk,))

    def __str__(self):
        return self.nombre + " (" + self.nif + ")"


class Empresa(models.Model):
    cod_pais = models.CharField(max_length=2)
    tipo_presentador = models.CharField(max_length=2, choices=TIPO_PRESENTADOR)
    nombre = models.CharField(max_length=256)
    nif = models.CharField(max_length=35, validators=[validate_nif])
    direccion = models.CharField(max_length=140)
    codpostal = models.CharField("cod. postal", max_length=10, validators=[validate_codpostal])
    poblacion = models.CharField(max_length=90)
    provincia = models.CharField(max_length=50)
    pais = models.CharField(max_length=30)
    iban = models.CharField("numero IBAN", max_length=34, validators=[validate_iban])
    bic = models.CharField("codigo BIC", max_length=11, validators=[validate_bic])

    def get_absolute_url(self):
        return reverse('serp:empresa-update', args=(self.pk,))

    def __str__(self):
        return self.nombre + " (" + self.nif + ")"


class Domiciliacion(models.Model):
    cliente = models.ForeignKey(Cliente)

    referencia = models.CharField(max_length=35)
    fecha_firma = models.DateField()
    recurrente = models.BooleanField()
    cdtr_nif = models.CharField("nif acreedor", max_length=35, validators=[validate_nif])
    cdtr_nombre = models.CharField("nombre acreedor", max_length=70)
    cdtr_direccion = models.CharField("dirección acreedor", max_length=140)
    cdtr_codpostal = models.CharField("cod. postal acreedor", max_length=10, validators=[validate_codpostal])
    cdtr_poblacion = models.CharField("población acreedor", max_length=90)
    cdtr_provincia = models.CharField("provincia acreedor", max_length=50)
    cdtr_pais = models.CharField("país acreedor", max_length=30)
    dbtr_nif = models.CharField("nif deudor", max_length=35, validators=[validate_nif])
    dbtr_nombre = models.CharField("nombre deudor", max_length=70)
    dbtr_direccion = models.CharField("dirección deudor", max_length=140)
    dbtr_codpostal = models.CharField("cod. postal deudor", max_length=10, validators=[validate_codpostal])
    dbtr_poblacion = models.CharField("población deudor", max_length=90)
    dbtr_provincia = models.CharField("provincia deudor", max_length=50)
    dbtr_bic = models.CharField("codigo BIC deudor", max_length=11, validators=[validate_bic])
    dbtr_iban = models.CharField("numero IBAN dudor", max_length=34, validators=[validate_iban])

    def get_absolute_url(self):
        return reverse('serp:domiciliacion-update', args=(self.pk,))

    def __str__(self):
        return self.referencia + " (" + str(self.fecha_firma) + ") " + ("RECURR" if self.recurrente else "UNIQUE")


class Servicio(models.Model):
    empresa = models.ForeignKey(Empresa)
    cliente = models.ForeignKey(Cliente)
    domiciliacion = models.ForeignKey(Domiciliacion)

    fecha = models.DateField("fecha")
    descripcion = models.CharField("descripcion", max_length=256)
    importe = models.DecimalField("importe", max_digits=5, decimal_places=2)
    periodicidad = models.IntegerField("periodicidad", choices=PERIODICIDAD)

    def __str__(self):
        return "%s - %s (%f, %d)" % (self.fecha, self.descripcion, self.importe, self. periodicidad)


class Cobro(models.Model):
    servicio = models.ForeignKey(Servicio)

    referencia = models.CharField(max_length=35)
    concepto = models.CharField(max_length=140)
    fecha = models.DateField()
    tipo = models.CharField(max_length=4, choices=TIPO_COBRO)
    importe = models.DecimalField(max_digits=5, decimal_places=2)

    def get_absolute_url(self):
        return reverse('serp:cobro-update', args=(self.pk,))

    def __str__(self):
        return "[%s] %s (%s)" % (self.tipo, self.concepto, self.fecha)


class Remesa(models.Model):
    cobros = models.ManyToManyField(Cobro)

    fecha = models.DateField("fecha")
