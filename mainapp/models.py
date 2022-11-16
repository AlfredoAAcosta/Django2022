from django.db import models

# Create your models here.
class Paciente(models.Model):
    nombre = models.CharField(max_length=30, verbose_name = "Nombre")
    apellido = models.CharField(max_length=30, verbose_name = "Apellido")
    celular = models.CharField(max_length=10)
	
class Turno(models.Model):
	fecha = models.DateField()
	hora = models.IntegerField()
	estado = models.BooleanField(default = False)
	paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)