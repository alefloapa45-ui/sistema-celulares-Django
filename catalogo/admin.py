# catalogo/admin.py

from django.contrib import admin
from .models import Marca, Celular, Reserva 

# Registrar la Marca
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Registrar el Celular 
@admin.register(Celular)
class CelularAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'marca', 'stock_actual', 'precio', 'created_at')
    list_filter = ('marca', 'created_at')
    search_fields = ('modelo', 'descripcion')
    list_editable = ('stock_actual', 'precio',) 

# Registrar la Reserva
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente_nombre', 'celular', 'cantidad', 'estado', 'fecha_reserva')
    list_filter = ('estado', 'fecha_reserva')
    search_fields = ('cliente_nombre', 'celular__modelo')
    list_editable = ('estado',)