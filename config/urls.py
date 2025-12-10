"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from menu.views import index, agregar_al_carrito, ver_carrito, limpiar_carrito, checkout, registro, mis_pedidos, contacto, ubicacion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registro/', registro, name='registro'),
    path('', index, name='index'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('limpiar/', limpiar_carrito, name='limpiar'),
    path('checkout/', checkout, name='checkout'),
    path('mis-pedidos/', mis_pedidos, name='mis_pedidos'),
    path('contacto/', contacto, name='contacto'),
    path('ubicacion/', ubicacion, name='ubicacion'),
]

# Configuración para servir imágenes en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)