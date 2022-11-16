from django.shortcuts import render
from datetime import datetime, date, timedelta
from mainapp.models import Paciente, Turno

# Create your views here.
def home(request):
    return render(request, "mainapp/home.html")

def turnos(request):
    turno_inicial = 16 # Horario del primer turno
    horario = []
    for n in range(0, 10): # 10 turnos de 30 minutos cada uno
        agregar = str(turno_inicial+n//2)+":"+str(30*(n%2))
        if len(agregar)==4:
            agregar = agregar+"0"
        horario.append(agregar)
    
    hoy = date.today()
    dia = date.weekday(hoy)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    fecha = []
    if dia > 4:
        dia_inicial = 7 - dia
        fecha_ini = hoy + timedelta(days= dia_inicial)
    else:
        dia_inicial = dia
        fecha_ini = hoy - timedelta(days= dia_inicial)
    for n in range(0, 5):
        dia_imprimir = fecha_ini+timedelta(days=n)
        fecha.append(dia_imprimir.day)
    
    turno_actual = Turno.objects.all()
    
    return render(request, "mainapp/turnos.html", {'horarios': horario, 'fechas': fecha, 'mes_turno': meses[fecha_ini.month], 'turnos': turno_actual, 'dias': [1,2,3,4,5]})

def registro(request):
    
    return render(request, "mainapp/registro.html")

def contact(request):
    return render(request, "mainapp/contact.html")