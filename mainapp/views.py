from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "mainapp/home.html")

def turnos(request):
    return render(request, "mainapp/turnos.html")

def registro(request):
    return render(request, "mainapp/registro.html")

def contact(request):
    return render(request, "mainapp/contact.html")