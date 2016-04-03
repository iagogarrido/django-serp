from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^clientes/$', views.ClienteListView.as_view(), name='cliente-list'),
    url(r'^clientes/create/$', views.ClienteCreateView.as_view(),
        name='cliente-create'),
    url(r'^clientes/(?P<pk>[0-9]+)/$', views.ClienteUpdateView.as_view(),
        name='cliente-update'),
    url(r'^clientes/(?P<pk>[0-9]+)/delete$', views.ClienteDeleteView.as_view(),
        name='cliente-delete'),
    url(r'^cobros/$', views.CobroListView.as_view(), name='cobro-list'),
    url(r'^cobros/create/$', views.CobroCreateView.as_view(),
        name='cobro-create'),
    url(r'^cobros/(?P<pk>[0-9]+)/$', views.CobroUpdateView.as_view(),
        name='cobro-update'),
    url(r'^cobros/(?P<pk>[0-9]+)/delete$', views.CobroDeleteView.as_view(),
        name='cobro-delete'),
    url(r'^sepa_xml/(?P<domiciliacion>[0-9]+)/$', views.SepaXmlView.as_view(),
        name='sepa-xml'),
    url(r'^empresas/(?P<pk>[0-9]+)/$', views.EmpresaUpdateView.as_view(),
        name='empresa-update'),
    url(r'^domiciliaciones/$', views.DomiciliacionListView.as_view(),
        name='domiciliacion-list'),
    url(r'^domiciliaciones/create/$', views.DomiciliacionCreateView.as_view(),
        name='domiciliacion-create'),
    url(r'^domiciliaciones/(?P<pk>[0-9]+)/$',
        views.DomiciliacionUpdateView.as_view(), name='domiciliacion-update'),
    url(r'^domiciliaciones/(?P<pk>[0-9]+)/delete$',
        views.DomiciliacionDeleteView.as_view(), name='domiciliacion-delete'),
]
