from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# TABLA MARCAS
class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre

# TABLA PRODUCTOS (Celulares)
class Celular(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    ram = models.CharField(max_length=20, verbose_name="Memoria RAM")
    almacenamiento = models.CharField(max_length=20, verbose_name="Almacenamiento Interno")
    camara = models.CharField(max_length=50, verbose_name="Cámara Principal")
    bateria = models.CharField(max_length=50, verbose_name="Batería")
    imagen = models.ImageField(upload_to='celulares/', null=True, blank=True)

    stock_actual = models.PositiveIntegerField(default=0)
    # aviso de stock bajo
    stock_minimo = models.PositiveIntegerField(default=2, verbose_name="Alerta Stock Mínimo")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.marca} - {self.modelo}"
    def bajo_stock(self):
        return self.stock_actual <= self.stock_minimo

# TABLA RESERVAS / APARTADOS
class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente de Retiro'),
        ('ENTREGADO', 'Entregado / Venta Finalizada'),
        ('CANCELADO', 'Cancelado / No recogido'),
    ]

    cliente_nombre = models.CharField(max_length=100)
    cliente_telefono = models.CharField(max_length=20)
    
    celular = models.ForeignKey(Celular, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_reserva = models.DateTimeField(default=timezone.now)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.cliente_nombre} - {self.celular.modelo}"