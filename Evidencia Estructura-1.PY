#Importacion de librerias
from collections import namedtuple
import os
from datetime import datetime as dt
import sys
from prettytable import PrettyTable
import csv

#Asignacion de variables
LimpiarPantalla = lambda: os.system('cls') #Funcion para limpiar pantalla
Servicio = namedtuple("Servicio", ("descripcion", "precio")) #Tupla nominada
monto_total = 0
diccionario_servicios = {}
lista_equipos = []

def separador():
    print("*" * 20) #Separador

try:
    with open('servicios.csv', newline='') as csv_doc:
        archivo_csv = csv.reader(csv_doc, delimiter=',')
        next(archivo_csv)
        contador = 1
        for linea in csv_doc:
            registro = linea.split(",") #Lista
            print(registro)
            if linea[0] == str(contador):
                clave_csv = int(registro[0])
                descripcion = registro[1]
                equipo = registro[2]
                precio = float(registro[3])
                fecha = registro[4]
                fecha = fecha.replace("\r\n","")
                cliente = registro[5]
                cliente = cliente.replace("\r\n","")
                equipo_registrado = Servicio(equipo, precio)
                lista_equipos.append(equipo_registrado)
            else:
                diccionario_servicios[clave_csv] = (lista_equipos.copy(),fecha,descripcion,cliente)
                lista_equipos.clear()

                clave_csv = int(registro[0])
                descripcion = registro[1]
                equipo = registro[2]
                precio = float(registro[3])
                fecha = registro[4]
                fecha = fecha.replace("\r\n","")
                cliente = registro[5]
                cliente = cliente.replace("\r\n","")
                equipo_registrado = Servicio(equipo, precio)
                lista_equipos.append(equipo_registrado)
                contador = contador + 1
        else:
            diccionario_servicios[clave_csv] = (lista_equipos.copy(),fecha,descripcion,cliente)
except:
    pass
while True:
    LimpiarPantalla()
    #Menu
    print("---MENU DE SERVICIOS---")
    print("¿Qué desea hacer?")
    print("A: Registrar un servicio")
    print("B: Consultar un servicio")
    print("C: Consultar a partir de una fecha")
    print("D: Grabar a CSV")
    print("E: Salir")
    try:
        opcion = input("Ingrese una opción: ")
        if opcion.upper() == "A":
            monto_total = 0
            switch = True
            servicio = int(input("Ingrese el folio del servicio: "))
            if servicio in diccionario_servicios.keys(): #valida si ya existe el servicio en el diccionario
                print("Ya existe el folio, ingree uno nuevo.")
                input("Pulse enter para cntinuar... ")
            else: 
                while switch:
                    while True:
                        equipo = input("Ingrese la descripción del equipo: ")
                        if equipo == "":
                            print("Este dato no puede ser vacío")
                        else:
                            break
                    while True:
                        try: #Valida que se ingrese un numero
                            precio = float(input("Ingrese el precio del equipo: "))
                        except Exception:
                            print(f"Ocurrió un problema, debe ingresar un dato numérico de tipo entero o float: {sys.exc_info()[0]}")
                            input("Pulse enter para continuar... ")
                        else:
                            break
                    
                    #A la variable equipo_registrado se le asigna el valor de la tupla
                    #-luego se agrega a la lista
                    equipo_registrado = Servicio(equipo, precio) 
                    lista_equipos.append(equipo_registrado)
                    monto_total = monto_total + precio

                    while True:
                        respuesta = int(input("¿Desea agregar otro equipo? 1=Sí 0=No: "))
                        if respuesta == 1:
                            LimpiarPantalla()
                            break
                        elif respuesta == 0:
                            switch = False
                            LimpiarPantalla()
                            while True:
                                nom_servicio = input("Ingrese descripcion de servicio: ")
                                if nom_servicio == "":
                                    print("No se puede omitir el nombre del servicio")
                                else:
                                    break
                            while True:
                                cliente = input("Ingrese el nombre del cliente: ")
                                if cliente == "":
                                    print("No se puede omitir el nombre del cliente")
                                else:
                                    break
                            #Se almacena la fecha, se calcula el monto, luego se carga al diccionario
                            fecha_procesada = dt.today().strftime('%d/%m/%Y')
                            IVA = (monto_total * 0.16)
                            print(f'El monto total a pagar por el servicio es: {"${:,.2f}".format((monto_total + IVA))}')
                            print(f'El IVA del 16% aplicado al total es: {"${:,.2f}".format((IVA))}')
                            lista_copia = lista_equipos.copy()
                            diccionario_servicios[servicio] = (lista_copia,fecha_procesada,nom_servicio,cliente)
                            lista_equipos.clear()
                            monto_total = 0
                            input("Pulse enter para continuar... ")
                            break
                        else:
                            print("Error. Opcion no válida!")
        elif opcion.upper() == "B":
            LimpiarPantalla()
            monto_total_consulta = 0
            busqueda = int(input("Ingrese el folio del servicio a buscar: "))
            if busqueda in diccionario_servicios.keys(): #Se valida que se encuentre la clave en el diccionario
                for equipo in diccionario_servicios[busqueda][0]: #En este ciclo se imprimen los datos
                    print(f"\nLa descripción del equipo es: {equipo[0]}")
                    print(f"El cobro del equipo fue: {equipo[1]}")
                    separador()
                    precio = equipo[1]
                    monto_total_consulta = monto_total_consulta + precio
                print(f"La fecha del servicio fue: {diccionario_servicios[busqueda][1]}")
                print(f"La descripción del servicio fue: {diccionario_servicios[busqueda][2]}")
                print(f"El cliente del servicio es: {diccionario_servicios[busqueda][3]}")
                IVA = monto_total_consulta * 0.16
                print(f"El monto total del servicio fue: {'${:,.2f}'.format(monto_total_consulta + IVA)}")
                print(f"El IVA del 16% aplicado al total fue: {'${:,.2f}'.format(IVA)}\n")
                separador()
                input("Pulse enter para continuar... ")
            else:
                print("El folio no se ha registrado. ")
                input("Pulse enter para continuar... ")

        elif opcion.upper() == "C":
            LimpiarPantalla()
            fecha_buscar = input("Ingrese la fecha a buscar (DD/MM/AAAA): ")
            for folio in diccionario_servicios.keys():
                monto_total_consulta = 0
                if fecha_buscar == diccionario_servicios[folio][1]: #Se valida que exista la fecha en el diccionario
                    separador()
                    print(f"FOLIO: {folio}")
                    t = PrettyTable(['Descripcion','Precio']) #Se utiliza prettytable para imprimir los datos
                    for equipo in diccionario_servicios[folio][0]:
                        t.add_row([equipo[0],equipo[1]])
                        monto = equipo[1]
                        monto_total_consulta = monto_total_consulta + monto
                    print(t)
                    print(f"La descripción del servicio fue: {diccionario_servicios[folio][2]}")
                    print(f"El cliente del servicio es: {diccionario_servicios[folio][3]}")
                    print(f"\nFecha del servicio: {diccionario_servicios[folio][1]}")
                    IVA = monto_total_consulta * 0.16
                    print(f"Monto total: {'${:,.2f}'.format(monto_total_consulta + IVA)}")
                    print(f"El IVA aplicado del 16% fue: {'${:,.2f}'.format(IVA)}")
                    separador()
                else:
                    print("No se encontraron servicios realizados en esa fecha.")
                    input("Pulse enter para continuar... ")
                    break
            else:
                input("\nPulse enter para continuar... ")
        elif opcion.upper()=="D":
            LimpiarPantalla()
            file_exists = os.path.isfile('servicios.csv')
            # Si el archivo existe, se abre y se sobrescribe la informacion
            if file_exists:
                with open('servicios.csv', mode='w+', newline='') as archivo_csv:
                        grabador = csv.writer(archivo_csv, delimiter=',')
                        grabador.writerow(['clave_servicio', 'descripcion', 'equipo', 'cobro', 'fecha', 'cliente'])
                        for clave in diccionario_servicios.keys():
                            servicio_csv = diccionario_servicios[clave][2]
                            fecha_csv = diccionario_servicios[clave][1]
                            cliente_csv = diccionario_servicios[clave][3]
                            for equipo in diccionario_servicios[clave][0]:
                                descripcion_csv = equipo[0]
                                cobro_csv = equipo[1]
                                grabador.writerow([clave, servicio_csv, descripcion_csv, cobro_csv, fecha_csv, cliente_csv])
            else:
                # Si el archivo no existe se crea incluyendo los encabezados
                with open('servicios.csv', mode='w', newline='') as archivo_csv:
                        grabador = csv.writer(archivo_csv, delimiter=',')
                        grabador.writerow(['clave_servicio', 'descripcion', 'equipo', 'precio', 'fecha', 'cliente'])
                        for clave in diccionario_servicios.keys():
                            servicio_csv = diccionario_servicios[clave][2]
                            fecha_csv = diccionario_servicios[clave][1]
                            cliente_csv = diccionario_servicios[clave][3]
                            for equipo in diccionario_servicios[clave][0]:
                                descripcion_csv = equipo[0]
                                cobro_csv = equipo[1]
                                grabador.writerow([clave, servicio_csv, descripcion_csv, cobro_csv, fecha_csv, cliente_csv])
            archivo_csv.close()
            print("Los datos se han cargado a CSV. ")
        elif opcion.upper() == "E":
            break
        else:
            print("Opcion no valida")
            input("Pulse enter para continuar... ")
    except ValueError:
        print('Ingrese un dato numérico entero. ')
        input("Pulse enter para continuar... ")
