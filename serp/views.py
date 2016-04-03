from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, \
    FormView

from . import sepa
from . import forms
from . import models

# Create your views here.

CLIENTE_FIELDS = [
    'referencia', 'nombre', 'nif', 'direccion', 'codpostal', 'poblacion',
    'provincia', 'email', 'bic', 'iban'
]

COBRO_FIELDS = [
    'servicio', 'referencia', 'concepto', 'fecha', 'tipo', 'importe'
]

EMPRESA_FIELDS = [
    'cod_pais', 'tipo_presentador', 'nombre', 'nif', 'direccion', 'codpostal',
    'poblacion', 'provincia', 'bic', 'iban'
]

DOMICILIACION_FIELDS = [
    'referencia', 'fecha_firma', 'recurrente', 'cdtr_nif', 'cdtr_nombre',
    'cdtr_direccion', 'cdtr_codpostal', 'cdtr_poblacion', 'cdtr_provincia',
    'cdtr_pais', 'dbtr_nif', 'dbtr_nombre', 'dbtr_direccion', 'dbtr_codpostal',
    'dbtr_poblacion', 'dbtr_provincia', 'dbtr_bic', 'dbtr_iban'
]


class IndexView(TemplateView):
    template_name = 'serp/base.html'


class ClienteListView(ListView):
    model = models.Cliente


class ClienteCreateView(CreateView):
    model = models.Cliente
    fields = CLIENTE_FIELDS


class ClienteUpdateView(UpdateView):
    model = models.Cliente
    fields = CLIENTE_FIELDS


class ClienteDeleteView(DeleteView):
    model = models.Cliente
    success_url = reverse_lazy('serp:cliente-list')


class CobroListView(ListView):
    model = models.Cobro
    tipo = ""

    def get_queryset(self):
        datos = super(self.__class__, self).get_queryset()
        self.tipo = self.request.GET.get('tipo')

        if self.tipo:
            datos_filtro = datos.filter(tipo=self.tipo)
        else:
            datos_filtro = datos

        return datos_filtro

    def get_context_data(self, **kwargs):
        contexto = super(self.__class__, self).get_context_data(**kwargs)
        cobros = self.object_list

        total = 0

        for cobro in cobros:
            if cobro.tipo == 'I':
                total += cobro.importe
            else:
                total -= cobro.importe

        contexto['total_base_imp'] = 0
        contexto['diferencia_base_imp'] = 0 * 21 / 100
        contexto['total_iva'] = 0
        contexto['total'] = total

        contexto['tipo'] = self.tipo

        return contexto


class CobroCreateView(CreateView):
    model = models.Cobro
    fields = COBRO_FIELDS


class CobroUpdateView(UpdateView):
    model = models.Cobro
    fields = COBRO_FIELDS


class CobroDeleteView(DeleteView):
    model = models.Cobro
    success_url = reverse_lazy('serp:cobro-list')


class SepaXmlView(FormView):
    form_class = forms.SepaTest
    template_name = 'serp/sepa_xml.html'

    def form_valid(self, form):
        id_domiciliacion = int(self.request.GET.get('domiciliacion'))

        domiciliacion = models.Domiciliacion.objects.get(pk=id_domiciliacion)

        return sepa.generate_content(domiciliacion, form.descripcion,
                                     form.importe)


class EmpresaUpdateView(UpdateView):
    model = models.Empresa
    fields = EMPRESA_FIELDS

    def get(self, request, **kwargs):
        pk = int(kwargs['pk'])

        if pk != 1:
            return HttpResponseForbidden('Acceso prohibido')
        else:
            return super(self.__class__, self).get(self, request, **kwargs)

    def get_queryset(self):
        if models.Empresa.objects.count() == 0:
            empresa = models.Empresa()
            empresa.save()

        return models.Empresa.objects.all()


class DomiciliacionListView(ListView):
    model = models.Domiciliacion


class DomiciliacionCreateView(CreateView):
    model = models.Domiciliacion
    fields = DOMICILIACION_FIELDS


class DomiciliacionUpdateView(UpdateView):
    model = models.Domiciliacion
    fields = DOMICILIACION_FIELDS


class DomiciliacionDeleteView(DeleteView):
    model = models.Domiciliacion
    success_url = reverse_lazy('serp:domiciliacion-list')
