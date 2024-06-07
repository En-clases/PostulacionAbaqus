from django.db import models

class Portafolio(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Activo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Precio(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    fecha = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.activo.nombre} - {self.fecha} - {self.precio}"

class Weight(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=4)
    
    def __str__(self):
        return f"{self.portafolio.nombre} - {self.activo.nombre} - {self.weight}"
