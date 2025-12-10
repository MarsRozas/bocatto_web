from django import forms
from .models import Pedido, MensajeContacto

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

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'correo', 'telefono', 'motivo', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9...'}),
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe aquí...'}),
        }