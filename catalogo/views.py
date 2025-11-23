from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField
from .models import Celular, Reserva, Marca
from .forms import ReservaForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required # Importación para proteger la vista

# VISTA DEL CATÁLOGO - Acceso Público
def catalogo(request):
    celulares = Celular.objects.filter(stock_actual__gt=0)
    query = request.GET.get('q')
    
    if query:
        celulares = celulares.filter(
            Q(modelo__icontains=query) | Q(marca__nombre__icontains=query)
        )
    
    context = {
        'celulares': celulares,
        'query': query
    }
    return render(request, 'catalogo/catalogo.html', context)


# VISTA DE GESTIÓN DE RESERVA - Acceso Público
def detalle_celular(request, pk):
    celular = get_object_or_404(Celular, pk=pk)
    
   
    form = ReservaForm() 

    if request.method == 'POST':
       
        form = ReservaForm(request.POST)
        if form.is_valid():
            
            cantidad_reservada = form.cleaned_data['cantidad']
            
            if cantidad_reservada > celular.stock_actual:
                messages.error(request, '¡Error! La cantidad solicitada supera el stock disponible.')
                return redirect('detalle_celular', pk=pk)

            if cantidad_reservada <= 0:
                messages.error(request, 'La cantidad debe ser mayor a cero.')
                return redirect('detalle_celular', pk=pk)

            # Crear la reserva
            reserva = form.save(commit=False)
            reserva.celular = celular
            reserva.save()
            # Actualizar Stock
            celular.stock_actual -= cantidad_reservada
            celular.save()
            
            messages.success(request, '✅ Reserva realizada con éxito! Tu celular ha sido apartado.')
            return redirect('catalogo')
    
    context = {
        'celular': celular,
        'form': form, 
    }
    return render(request, 'catalogo/detalle_celular.html', context)


# DASHBOARD ADMINISTRATIVO - Acceso Privado 
@login_required 
def dashboard_admin(request):
    
    alerta_stock = Celular.objects.filter(stock_actual__lte=F('stock_minimo'))

    #Reporte Semanal 
    hace_siete_dias = timezone.now() - timedelta(days=7)
    reservas_semanales = Reserva.objects.filter(fecha_reserva__gte=hace_siete_dias)

    #Reporte de Reservas Pendientes
    reservas_pendientes = Reserva.objects.filter(estado='PENDIENTE').order_by('fecha_reserva')
    
    ventas_semanales = reservas_semanales.filter(estado='ENTREGADO').count()
    total_reservas = reservas_semanales.count()
    
    valor_pendiente = Reserva.objects.filter(estado='PENDIENTE').aggregate(
        valor=Sum(ExpressionWrapper(F('cantidad') * F('celular__precio'), output_field=DecimalField()))
    )['valor']

    context = {
        'alerta_stock': alerta_stock,
        'reservas_pendientes': reservas_pendientes,
        'ventas_semanales': ventas_semanales,
        'total_reservas_semana': total_reservas,
        'valor_pendiente': valor_pendiente or 0,
    }
    return render(request, 'catalogo/dashboard_admin.html', context)

@login_required 
def tutoriales(request):
    """Vista para el módulo de capacitación (videos y ayuda)."""

    videos = [
        {'titulo': 'Cómo Usar el Dashboard y las Alertas', 'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ?si=xX8dK2jR0f8R0f8R', 'descripcion': 'Guía rápida para entender las métricas y alertas de stock.'},
        {'titulo': 'Gestión de Reservas y Actualización de Stock', 'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ?si=xX8dK2jR0f8R0f8R', 'descripcion': 'Aprende a confirmar la entrega o cancelación de un pedido.'},
        {'titulo': 'Guía de Subida de Nuevos Productos', 'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ?si=xX8dK2jR0f8R0f8R', 'descripcion': 'Tutorial para ingresar marcas y modelos al sistema.'},
    ]
    
    context = {'videos': videos}
    return render(request, 'catalogo/tutoriales.html', context)

@login_required 
def confirmar_reserva(request, pk):
    """Marca la reserva como ENTREGADO y no afecta el stock, ya que se redujo al reservar."""
    reserva = get_object_or_404(Reserva, pk=pk)
    
    if reserva.estado != 'PENDIENTE':
        messages.warning(request, f'⚠️ La reserva ya fue marcada como "{reserva.estado}". No se realizaron cambios.')
        return redirect('dashboard_admin')
        
    #Cambiar estado
    reserva.estado = 'ENTREGADO'
    reserva.save()
    
    messages.success(request, f'✅ Reserva #{pk} confirmada y entregada al cliente {reserva.cliente_nombre}.')
    return redirect('dashboard_admin')

@login_required 
def cancelar_reserva(request, pk):
    """Marca la reserva como CANCELADO y RESTABLECE el stock del celular."""
    reserva = get_object_or_404(Reserva, pk=pk)
    celular = reserva.celular
    
    #Verificar estado actual
    if reserva.estado != 'PENDIENTE':
        messages.warning(request, f'⚠️ La reserva ya fue marcada como "{reserva.estado}". No se realizaron cambios.')
        return redirect('dashboard_admin')

    #Cambiar estado
    reserva.estado = 'CANCELADO'
    reserva.save()
    #Restablecer Stock
    cantidad_restablecida = reserva.cantidad
    celular.stock_actual += cantidad_restablecida
    celular.save()
    
    messages.info(request, f'❌ Reserva #{pk} cancelada. Se restablecieron {cantidad_restablecida} unidades de {celular.modelo} al inventario.')
    return redirect('dashboard_admin')