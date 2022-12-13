from django.contrib import admin
from .models import Paciente, Turno

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Turno)