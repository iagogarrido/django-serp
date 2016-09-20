from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
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
    'poblacion', 'provincia', 'bic', 'iban', 'presentador'
]

DOMICILIACION_FIELDS = [
    'referencia', 'fecha_firma', 'recurrente', 'cdtr_nif', 'cdtr_nombre',
    'cdtr_direccion', 'cdtr_codpostal', 'cdtr_poblacion', 'cdtr_provincia',
    'cdtr_pais', 'dbtr_nif', 'dbtr_nombre', 'dbtr_direccion', 'dbtr_codpostal',
    'dbtr_poblacion', 'dbtr_provincia', 'dbtr_bic', 'dbtr_iban'
]

SERVICIO_FIELDS = [
    'cliente', 'fecha', 'descripcion', 'importe', 'periodicidad'
]

REMESA_FIELDS = [
    'presentador', 'referencia', 'fecha'
]


class IndexView(TemplateView):
    template_name = 'serp/base.html'


# ----- CLIENTES -----

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


# ----- COBRO -----

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


# ----- EMPRESA -----

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


# ----- DOMICILIACION -----

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


# ----- SERVICIO -----

class ServicioListView(ListView):
    model = models.Servicio
    model_name = 'servicio'

    def get_queryset(self):
        pk_cliente = self.kwargs.get('pk_cliente')

        if pk_cliente:
            cliente = get_object_or_404(models.Cliente, pk=pk_cliente)
            datos = self.model.objects.filter(cliente=cliente)
        else:
            datos = super(self.__class__, self).get_queryset()

        return datos

    def get_context_data(self, **kwargs):
        pk_cliente = self.kwargs.get('pk_cliente')

        if pk_cliente:
            self.model_name = 'cliente-servicio'
            self.pk_cliente = pk_cliente

        kwargs['model_name'] = self.model_name

        return super(self.__class__, self).get_context_data(**kwargs)


class ServicioCreateView(CreateView):
    model = models.Servicio
    fields = SERVICIO_FIELDS

    pk_refs_fields = [('pk_cliente', 'cliente')]

    def get_context_data(self, **kwargs):
        if 'pk_refs' not in kwargs:
            for pk_ref, _ in self.pk_refs_fields:
                if pk_ref in self.kwargs:
                    kwargs[pk_ref] = self.kwargs[pk_ref]

        return super(self.__class__, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        form = super(self.__class__, self).get_form(form_class=form_class)

        for pk_ref, field_ref in self.pk_refs_fields:
            if pk_ref in self.kwargs:
                if field_ref in form.fields:
                    form.initial[field_ref] = self.kwargs[pk_ref]
                    form.fields[field_ref].widget.attrs['disabled'] = True

        return form

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()

        for pk_ref, field_ref in self.pk_refs_fields:
            if (pk_ref in kwargs) and (field_ref not in data):
                data[field_ref] = str(kwargs[pk_ref])

        request.POST = data

        return super(self.__class__, self).post(request, *args, **kwargs)


# ----- REMESA -----

class RemesaListView(ListView):
    model = models.Remesa


class RemesaCreateView(CreateView):
    model = models.Remesa
    fields = REMESA_FIELDS
