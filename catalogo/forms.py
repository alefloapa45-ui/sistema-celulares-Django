# catalogo/forms.py

from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente_nombre', 'cliente_telefono', 'cantidad']
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}),
            'cliente_telefono': forms.TextInput(attrs={'placeholder': 'Teléfono de contacto'}),
        }