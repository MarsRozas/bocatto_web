from django.contrib import admin
from .models import Categoria, Producto, Pedido, ItemPedido
# Register your models here.

admin.site.register(Categoria)
admin.site.register(Producto)

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0  # Para que no muestre filas vacías extra
    readonly_fields = ('producto', 'cantidad', 'precio') # Para que no se modifiquen por error
    can_delete = False

class PedidoAdmin(admin.ModelAdmin):
    # Estas son las columnas que verás en la lista general de pedidos
    list_display = ('id', 'nombre_cliente', 'estado', 'fecha', 'tipo_entrega', 'total', 'pagado')
    
    # Filtros laterales para buscar rápido
    list_filter = ('estado', 'fecha')

    #Permite cambiar el estado desde la lista
    list_editable = ('estado', 'pagado')
    
    # Barra de búsqueda
    search_fields = ('nombre_cliente', 'id')
    
    # Aquí conectamos los items para verlos dentro del pedido
    inlines = [ItemPedidoInline]
    
    # Hacemos que la fecha sea solo lectura para que nadie "truque" cuándo se pidió
    readonly_fields = ('fecha',)

# Registramos el Pedido con esta configuración especial
admin.site.register(Pedido, PedidoAdmin)