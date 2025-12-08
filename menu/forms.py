from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_cliente', 'telefono', 'tipo_entrega', 'direccion']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_entrega': forms.Select(attrs={'class': 'form-select', 'id': 'tipoEntrega'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'inputDireccion'}),
        }