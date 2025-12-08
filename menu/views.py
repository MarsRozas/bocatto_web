from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto, Pedido, ItemPedido
from .forms import PedidoForm
from django.contrib.auth.forms import UserCreationForm # <--- Para crear usuarios
from django.contrib.auth.decorators import login_required # <--- El candado
from django.contrib import messages
# Create your views here.

@login_required
def index(request):
    # Obtenemos todas las categorías, y gracias a 'related_name' en el modelo,
    # podremos acceder a sus productos en el HTML.
    categorias = Categoria.objects.all()
    return render(request, 'menu/index.html', {'categorias': categorias})

@login_required
def agregar_al_carrito(request, producto_id):
    # 1. Obtenemos el carrito actual de la sesión, o creamos uno vacío {}
    carrito = request.session.get('carrito', {})
    
    # 2. Convertimos el ID a string (JSON usa strings como claves)
    producto_id = str(producto_id)

    # 3. Si el producto ya está, sumamos 1. Si no, lo iniciamos en 1.
    if producto_id in carrito:
        carrito[producto_id] += 1
    else:
        carrito[producto_id] = 1

    # 4. Guardamos el carrito actualizado en la sesión
    request.session['carrito'] = carrito
    
    # 5. Redireccionamos a la página del carrito (como pediste)
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    # Recuperamos el diccionario de IDs y cantidades
    carrito_session = request.session.get('carrito', {})
    
    items_carrito = []
    total_general = 0

    # Buscamos los objetos reales en la base de datos
    for producto_id, cantidad in carrito_session.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total_general += subtotal
        
        # Creamos una estructura temporal para pasarla al HTML
        items_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })

    return render(request, 'menu/carrito.html', {
        'items_carrito': items_carrito, 
        'total_general': total_general
    })

def limpiar_carrito(request):
    # Función útil para borrar todo si se equivocan
    if 'carrito' in request.session:
        del request.session['carrito']
    return redirect('ver_carrito')

@login_required
def checkout(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        return redirect('index') # Si no hay nada, patada al inicio

    # Calcular total para mostrarlo (aunque se recalcula al guardar)
    total_general = 0
    items_checkout = []
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        subtotal = producto.precio * cantidad
        total_general += subtotal
        items_checkout.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # 1. Guardar la info del cliente pero NO en base de datos todavía (commit=False)
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.total = total_general
            pedido.pagado = True # Simulamos que pagó correctamente
            pedido.save() # Ahora sí guardamos y tenemos un ID de pedido

            # 2. Guardar cada item del carrito en la base de datos
            for item in items_checkout:
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                    precio=item['producto'].precio
                )

            # 3. Limpiar carrito y redirigir
            del request.session['carrito']
            return render(request, 'menu/exito.html', {'id_pedido': pedido.id})
    else:
        form = PedidoForm()

    return render(request, 'menu/checkout.html', {
        'form': form, 
        'items': items_checkout, 
        'total': total_general
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. ¡Ahora ingresa!')
            return redirect('login') # Redirige al login de Django
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def mis_pedidos(request):
    # Filtramos los pedidos que pertenecen al usuario logueado
    # Ojo: Esto asume que guardaste el usuario en el checkout.
    # Si usas nombre_cliente, tendrías que filtrar por eso, pero lo ideal es por request.user
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'menu/mis_pedidos.html', {'pedidos': pedidos})