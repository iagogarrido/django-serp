from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import sepa
from . import models


# Create your views here.

PERSONA_FIELDS = [
    'referencia', 'nombre', 'nif', 'email', 'bic', 'iban'
]

COBRO_FIELDS = [
    'persona', 'referencia', 'concepto', 'fecha', 'tipo', 'base_imponible',
    'iva'
]

EMPRESA_FIELDS = [
    'cod_pais', 'tipo_presentador', 'nombre', 'nif', 'bic', 'iban'
]


class IndexView(TemplateView):
    template_name = 'serp/base.html'


class PersonaListView(ListView):
    model = models.Persona


class PersonaCreateView(CreateView):
    model = models.Persona
    fields = PERSONA_FIELDS


class PersonaUpdateView(UpdateView):
    model = models.Persona
    fields = PERSONA_FIELDS


class PersonaDeleteView(DeleteView):
    model = models.Persona
    success_url = reverse_lazy('serp:persona-list')


class CobroListView(ListView):
    model = models.Cobro
    allow_sepa = False

    def get_queryset(self):
        datos = super(self.__class__, self).get_queryset()
        tipo = self.request.GET.get('tipo')

        if tipo:
            if tipo == 'I':
                self.allow_sepa = True

            datos_filtro = datos.filter(tipo=tipo)
        else:
            datos_filtro = datos

        return datos_filtro

    def get_context_data(self, **kwargs):
        contexto = super(self.__class__, self).get_context_data(**kwargs)
        cobros = self.object_list

        total_base_imp = 0
        total_iva = 0
        total = 0

        for cobro in cobros:
            if cobro.tipo == 'I':
                total_base_imp += cobro.base_imponible
                total_iva += cobro.cuota_iva
                total += cobro.total
            else:
                total_base_imp -= cobro.base_imponible
                total_iva -= cobro.cuota_iva
                total -= cobro.total

        contexto['total_base_imp'] = total_base_imp
        contexto['diferencia_base_imp'] = total_base_imp * 21 / 100
        contexto['total_iva'] = total_iva
        contexto['total'] = total

        contexto['allow_sepa'] = self.allow_sepa

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


class SepaXmlView(View):
    def get(self, request):
        return sepa.generate_content(
                {'count': models.Cobro.objects.filter(tipo='I').count()})


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
