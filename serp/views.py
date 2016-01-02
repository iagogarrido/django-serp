from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Persona, Cobro

# Create your views here.

PERSONA_FIELDS = [
    'referencia', 'nombre', 'nif', 'email'
]

COBRO_FIELDS = [
    'persona', 'referencia', 'concepto', 'fecha', 'tipo', 'base_imponible',
    'iva'
]


class IndexView(TemplateView):
    template_name = 'serp/base.html'


class PersonaListView(ListView):
    model = Persona


class PersonaCreateView(CreateView):
    model = Persona
    fields = PERSONA_FIELDS


class PersonaUpdateView(UpdateView):
    model = Persona
    fields = PERSONA_FIELDS


class PersonaDeleteView(DeleteView):
    model = Persona
    success_url = reverse_lazy('serp:persona-list')


class CobroListView(ListView):
    model = Cobro

    def get_queryset(self):
        datos = super(self.__class__, self).get_queryset()
        tipo = self.request.GET.get('tipo')

        if tipo:
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

        return contexto


class CobroCreateView(CreateView):
    model = Cobro
    fields = COBRO_FIELDS


class CobroUpdateView(UpdateView):
    model = Cobro
    fields = COBRO_FIELDS


class CobroDeleteView(DeleteView):
    model = Cobro
    success_url = reverse_lazy('serp:cobro-list')
