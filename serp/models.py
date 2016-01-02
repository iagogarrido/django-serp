from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

TIPO_COBRO = (
    ('I', 'Ingreso'),
    ('G', 'Gasto'),
)


class Persona(models.Model):
    referencia = models.CharField(max_length=128)
    nombre = models.CharField(max_length=256)
    nif = models.CharField(max_length=10)
    email = models.CharField(max_length=256)

    def get_absolute_url(self):
        return reverse('serp:persona-update', args=(self.pk,))

    def __str__(self):
        return self.nombre + " (" + self.nif + ")"


class Cobro(models.Model):
    persona = models.ForeignKey(Persona)
    referencia = models.CharField(max_length=128)
    concepto = models.CharField(max_length=256)
    fecha = models.DateField()
    tipo = models.CharField(max_length=4, choices=TIPO_COBRO)
    base_imponible = models.FloatField()
    iva = models.FloatField()

    @property
    def cuota_iva(self):
        return self.base_imponible * self.iva / 100

    @property
    def total(self):
        return self.base_imponible + self.cuota_iva

    def get_absolute_url(self):
        return reverse('serp:cobro-update', args=(self.pk,))

    def __str__(self):
        return "[%s] %s (%s)" % (self.tipo, self.concepto, self.fecha)
