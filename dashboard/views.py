from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usuarioL.models import usuarioL
from .forms import ExcelForm, RegistroForm, RegistroNewForm
from usuario.models import RescatePunto, EstadoFuerza, PuntosInternacion, Municipios, Paises
from django.contrib import messages
import datetime

# Create your views here.
@login_required
def dashboard(request):

    if request.method == 'GET':
        form = ExcelForm()
        userDataI = usuarioL.objects.filter(user__username=request.user)
        data = {
            'usuario' : userDataI,
            'form': form,
        }
        return render(request, "dashboard/dashboard.html", context=data)
    
    elif request.method == 'POST':
        userDataI = usuarioL.objects.filter(user__username=request.user)
        form = ExcelForm(request.POST)
        if(form.is_valid()):
            dia = request.POST["fechaDescarga_day"]
            mes = request.POST["fechaDescarga_month"]
            year = request.POST["fechaDescarga_year"]

            fechaR = datetime.datetime.strptime(f"{dia}/{mes}/{year}", "%d/%m/%Y").strftime('%d-%m-%y')

            valores = RescatePunto.objects.filter(fecha=fechaR).filter(oficinaRepre=userDataI[0].oficinaR)

        data = {
            'usuario' : userDataI,
            'form': form,
            'values' : valores,
        }

        return render(request, "dashboard/dashboard.html", context=data)

    else: 
        form = ExcelForm()
        userDataI = usuarioL.objects.filter(user__username=request.user)
        data = {
            'usuario' : userDataI,
            'form': form,
        }
        return render(request, "dashboard/dashboard.html", context=data) 
    

def editarData(request, pk):
    if request.user.is_authenticated:
        rescate = RescatePunto.objects.get(idRescate=pk)
        if request.method == 'GET':
            # userDataI = usuarioL.objects.filter(user__username=request.user)
            ofiRep = str(rescate.oficinaRepre)

            types_PRescateA = []
            types_PRescateC = []
            types_PRescateCA = []
            types_PRescateF = []
            types_PRescateM = []
            types_Naciona = []

            for punt in PuntosInternacion.objects.filter(estadoPunto=ofiRep, tipoPunto="AEREOS"):
                nomS = str(punt.nombrePunto)
                types_PRescateA.append(nomS.strip())

            for mun in Municipios.objects.filter(estado=ofiRep):
                nomS = str(mun.nomMunicipio)
                types_PRescateM.append(nomS.strip())

            for nac in Paises.objects.all():
                nomS = str(nac.nombre_pais)
                types_Naciona.append(nomS.strip())

            for puntos in EstadoFuerza.objects.filter(oficinaR=ofiRep):
                nomS = str(puntos.nomPuntoRevision)
                if puntos.tipoP == "Carretero":
                    types_PRescateC.append(nomS.strip())
                elif puntos.tipoP == "Central de autobús":
                    types_PRescateCA.append(nomS.strip())
                elif puntos.tipoP == "Ferroviario":
                    types_PRescateF.append(nomS.strip())
                else:
                    # print(nomS)
                    pass

            puntoR = ""
            if rescate.aeropuerto:
                puntoR = 'aeropuerto'
            elif rescate.carretero:
                puntoR = 'carretero'
            elif rescate.centralAutobus:
                puntoR = 'central de autobus'
            elif rescate.casaSeguridad:
                puntoR = 'casa de seguridad'
            elif rescate.ferrocarril:
                puntoR = 'ferrocarril'
            elif rescate.hotel:
                puntoR = 'hotel'
            elif rescate.puestosADispo:
                puntoR = 'puestos a disposicion'
            elif rescate.voluntarios:
                puntoR = 'voluntarios'
            else: 
                puntoR = ''

            fecha_Naci = datetime.datetime.strptime(rescate.fechaNacimiento, "%d/%m/%Y").strftime('%Y-%m-%d')
            
            datosR = {
                'idRescate': pk,
                'fecha': rescate.fecha,
                'hora': rescate.hora,
                'tipo_punto' : puntoR,
                'puntoEstra': rescate.puntoEstra,
                'nacionalidad': rescate.nacionalidad,
                'nombre': rescate.nombre,
                'apellidos': rescate.apellidos,
                'parentesco': rescate.parentesco,
                'fechaNacimiento': fecha_Naci,
                'sexo': rescate.sexo,
                'embarazo': rescate.embarazo,
                'numFamilia': rescate.numFamilia,
            }
            
            form = RegistroNewForm(initial=datosR)
            # print(types_PRescateC)
            datos = {
                "form" : form,
                "value": rescate,
                "datosR": datosR,
                "res_aero": types_PRescateA,
                "res_carre": types_PRescateC,
                "res_central": types_PRescateCA,
                "res_ferro": types_PRescateF,
                "municipio": types_PRescateM,
                "nacion": types_Naciona,
            }
            
            return render(request, "dashboard/editarDato.html", context=datos )
        if request.method == 'POST':
            form = RegistroNewForm(request.POST)
            datos = {
                "form" : form,
                "value": rescate,
            }
            if form.is_valid():
                form.save()
                messages.success(request, "El registro ha sido modificado")
                return redirect('../datos/')
            else:
                print("datos erroneos")
                messages.success(request, "Datos Erroneos")
                return render(request, "dashboard/editarDato.html", context=datos )
            
    else:
        messages.success(request, "Necesitas ingresar para poder modificar la informacion")
        return redirect('')

def mostrarData(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            userDataI = usuarioL.objects.filter(user__username=request.user)
            
            form = ExcelForm(request.POST)
            form1 = RegistroNewForm(request.POST)
            
            if(form.is_valid()):
                dia = request.POST["fechaDescarga_day"]
                mes = request.POST["fechaDescarga_month"]
                year = request.POST["fechaDescarga_year"]

                fechaR = datetime.datetime.strptime(f"{dia}/{mes}/{year}", "%d/%m/%Y").strftime('%d-%m-%y')

                if request.user.is_superuser:
                    valores = RescatePunto.objects.filter(fecha=fechaR)

                    data = {
                    'usuario' : userDataI,
                    'form': form,
                    'values' : valores,
                    'fecha_P' : fechaR,
                    }

                    return render(request, "dashboard/datos_diaSU.html", context=data)
                else:
                    valores = RescatePunto.objects.filter(fecha=fechaR).filter(oficinaRepre=userDataI[0].oficinaR)

                    data = {
                    'usuario' : userDataI,
                    'form': form,
                    'values' : valores,
                    'fecha_P' : fechaR,
                    }

                    return render(request, "dashboard/datos_dia.html", context=data)

            if form1.is_valid():
                fechaR = request.POST["fecha"]
                form1.save()

                if request.user.is_superuser:
                    valores = RescatePunto.objects.filter(fecha=fechaR)
                else:
                    valores = RescatePunto.objects.filter(fecha=fechaR).filter(oficinaRepre=userDataI[0].oficinaR)

                data = {
                'usuario' : userDataI,
                'form': form,
                'values' : valores,
                }
                messages.success(request, "El registro ha sido modificado")
                return render(request, "dashboard/datos_dia.html", context=data)
            else:
                print("datos erroneos")
                print(form1.errors)
                idR = request.POST["idRescate"]
                rescate = RescatePunto.objects.get(idRescate=idR)
                datos = {
                "form" : form1,
                "value": rescate,
                }
                messages.success(request, "Datos Erroneos")
                return render(request, "dashboard/editarDato.html", context=datos )


    else:
        messages.success(request, "Necesitas ingresar para poder modificar la informacion")
        return redirect('')



# def update_record(request, pk):
#     if request.user.is_authenticated:
#         registro = RescatePunto.objects.get(idRescate=pk)
#         form = addRegistro(request.POST or None, instance = registro)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "El registro ha sido modificado")
#             redirect('dashboard')
#         return render(request, 'dashboard/editarDato.html', {'form' : form})
#     else: 
#         messages.success(request, "Necesitas ingresar para poder modificar la informacion")
#         return redirect('')