from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime, date, timedelta
from mainapp.models import Paciente, Turno
from .forms import PacienteForm, RegistrarUsuarioForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
cont_semana = 0
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
    fecha_completa = []
    if dia > 4:
        dia_inicial = 7 - dia
        fecha_ini = hoy + timedelta(days= dia_inicial)
    else:
        dia_inicial = dia
        fecha_ini = hoy - timedelta(days= dia_inicial)

    fecha_ini = fecha_ini + timedelta(days= cont_semana)
    for n in range(0, 5):
        dia_imprimir = fecha_ini+timedelta(days=n)
        fecha.append(dia_imprimir.day)
        fecha_completa.append(dia_imprimir)
    
    fila = 0
    columna = 0
    fecha_final = fecha_ini + timedelta(days=4)
    turnos_semana = [["" for c in range(5)] for f in range(10)]
    turno_actual = Turno.objects.all()
    for n in turno_actual:
        for c in range(5):
            if n.fecha == fecha_completa[c]:
                columna = c
        for f in range(10):
            if n.hora == horario[f]:
                fila = f
        if n.fecha >= fecha_completa[0] and n.fecha <= fecha_completa[4]:
            turnos_semana[fila][columna]="1"
    #print(turnos_semana)
    #print(fecha[2])
    return render(request, "mainapp/turnos.html", {'horarios': horario, 'fechas': fecha, 'mes_turno': meses[fecha_ini.month-1], 'turnos': turnos_semana})

def adelante(request):
    global cont_semana
    cont_semana += 7
    return redirect('turnos')

def atras(request):
    global cont_semana
    cont_semana -= 7
    return redirect('turnos')


#ef registro(request):
#    return render(request, "mainapp/registro.html")

def contact(request):
    return render(request, "mainapp/contact.html")

class PacienteView(View):
    form_class = PacienteForm
    template_name = 'mainapp/registro.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'formulario': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portada')

        return render(request, self.template_name, {'formulario': form})


def registrarse(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tu cuenta fue creada con éxito! Ya te podes loguear en el sistema.')
            return redirect('login')
    else:
        form = RegistrarUsuarioForm()
    return render(request, 'mainapp/registrarse.html', {'form': form, 'title': 'registrese aquí'})

def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' Bienvenido/a {username} !!')
            return redirect('registro')
        else:
            messages.error(request, f'Cuenta o Password incorrecto !')
    form = AuthenticationForm()
    return render(request, 'mainapp/login.html', {'form': form, 'title': 'Log in'})

