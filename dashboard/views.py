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

def datos_fecha(request):
    if request.method == 'POST':
        form = ExcelForm(request.POST)
        if form.is_valid():
            # Obtiene la fecha seleccionada del formulario
            fecha_seleccionada = form.cleaned_data['fechaDescarga']
            # Redirige a la vista de la tabla de productos con la fecha seleccionada
            return redirect('tabla_registros_fecha', year=fecha_seleccionada.year, month=fecha_seleccionada.month, day=fecha_seleccionada.day)
    else:
        return redirect('/dashboard')
    
def eliminar_registros(request):
    if request.method == 'POST':
        # Obtén los IDs de los productos seleccionados
        registros_seleccionados = request.POST.getlist('registros_seleccionados')

        # Elimina los productos seleccionados
        registros_eliminar = RescatePunto.objects.filter(idRescate__in=registros_seleccionados)
        fechaR = registros_eliminar[0].fecha
        registros_eliminar.delete()

        # Redirige a la página de la tabla de productos o a donde desees
        fecha_seleccionada = datetime.datetime.strptime(f"{fechaR}", "%d-%m-%y")
                # return redirect('../datos/')
        return redirect('tabla_registros_fecha', year=fecha_seleccionada.year, month=fecha_seleccionada.month, day=fecha_seleccionada.day)

    # Obtén todos los productos para mostrar en la tabla
    return redirect("/dashboard")

def tabla_registros(request, year=None, month=None, day=None):
    
    userDataI = usuarioL.objects.filter(user__username=request.user)
    fechaR = datetime.datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y").strftime('%d-%m-%y')
    form = ExcelForm()
    
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

            tiposPNombre = [
                'aeropuerto',
                'carretero',
                'central de autobus',
                'casa de seguridad',
                'ferrocarril',
                'hotel',
                'puestos a disposición',
                'voluntarios',
            ]

            puntoR = ""
            if rescate.aeropuerto:
                puntoR = tiposPNombre[0]
            elif rescate.carretero:
                puntoR = tiposPNombre[1]
            elif rescate.centralAutobus:
                puntoR = tiposPNombre[2]
            elif rescate.casaSeguridad:
                puntoR = tiposPNombre[3]
            elif rescate.ferrocarril:
                puntoR = tiposPNombre[4]
            elif rescate.hotel:
                puntoR = tiposPNombre[5]
            elif rescate.puestosADispo:
                puntoR = tiposPNombre[6]
            elif rescate.voluntarios:
                puntoR = tiposPNombre[7]
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
                'tiposPNombre': tiposPNombre,
            }

            # print(ofiRep)
            # print(types_PRescateA)
            # print(rescate.puntoEstra)
            
            return render(request, "dashboard/editarDato.html", context=datos )
        if request.method == 'POST':
            form = RegistroNewForm(request.POST)
            datos = {
                "form" : form,
                "value": rescate,
            }
            if form.is_valid():
                form.save()
                fecha_form = form.cleaned_data['fecha']
                # print("entra a guardar info")
                # print(fecha_form)
                messages.success(request, "El registro ha sido modificado")
                fecha_seleccionada = datetime.datetime.strptime(f"{fecha_form}", "%d-%m-%y")
                # return redirect('../datos/')
                return redirect('tabla_registros_fecha', year=fecha_seleccionada.year, month=fecha_seleccionada.month, day=fecha_seleccionada.day)
            else:
                print(form.errors)
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