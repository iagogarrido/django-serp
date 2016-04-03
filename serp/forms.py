from django import forms


class SepaTest(forms.Form):
    descripcion = forms.CharField(max_length=140)
    importe = forms.DecimalField(decimal_places=2)
    fecha = forms.DateField()
