from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0) # Usamos 0 decimales si es CLP
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

class Pedido(models.Model):
    TIPOS_ENTREGA = [
        ('retiro', 'Retiro en Tienda'),
        ('delivery', 'Delivery'),
    ]
    ESTADOS = [
        ('recibido', 'Pedido Recibido'),
        ('preparacion', 'En Preparación'),
        ('despacho', 'En Despacho'),
        ('entregado', 'Entregado'),
    ]

    nombre_cliente = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    tipo_entrega = models.CharField(max_length=20, choices=TIPOS_ENTREGA, default='retiro')
    direccion = models.TextField(blank=True, null=True) # Opcional, solo si es delivery
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    pagado = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='recibido')

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente}"
    
    def get_progreso_step(self):
        orden = {'recibido': 1, 'preparacion': 2, 'despacho': 3, 'entregado': 4}
        return orden.get(self.estado, 1)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=0) # Guardamos el precio del momento

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"