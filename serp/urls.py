from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^personas/$', views.PersonaListView.as_view(), name='persona-list'),
    url(r'^personas/create/$', views.PersonaCreateView.as_view(), name='persona-create'),
    url(r'^personas/(?P<pk>[0-9]+)/$', views.PersonaUpdateView.as_view(), name='persona-update'),
    url(r'^personas/(?P<pk>[0-9]+)/delete$', views.PersonaDeleteView.as_view(), name='persona-delete'),
    url(r'^cobros/$', views.CobroListView.as_view(), name='cobro-list'),
    url(r'^cobros/create/$', views.CobroCreateView.as_view(), name='cobro-create'),
    url(r'^cobros/(?P<pk>[0-9]+)/$', views.CobroUpdateView.as_view(), name='cobro-update'),
    url(r'^cobros/(?P<pk>[0-9]+)/delete$', views.CobroDeleteView.as_view(), name='cobro-delete'),
]
