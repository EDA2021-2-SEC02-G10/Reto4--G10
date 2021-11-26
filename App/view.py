﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
assert cf
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

default_limit = 10000 
sys.setrecursionlimit(default_limit*10)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printResults1(analyzer, result):

    lst1 = result[0]
    lst2 = result[1]
    top1 = result[2]
    top2 = result[3]
    print('Para el grafo dirigido, el (los) aeropuerto(s) con mas interconexiones tienen: ')
    print(str(top1) + ' interconexiones')
    print('Los aeropuertos con este numero de interconexiones son: ')
    for airport in lt.iterator(lst1):
        print(airport)
        name = (list(airport.keys()))[0]
        print(name)
        dataEntry = mp.get(analyzer['airportsMap'], name)
        data = me.getValue(dataEntry)
        print(data)

    print('Para el grafo no dirigido, el (los) aeropuerto(s) con mas interconexiones tienen: ')
    print(str(top2) + ' interconexiones')
    print('Los aeropuertos con este numero de interconexiones son: ')
    for airport in lt.iterator(lst2):
        name = (list(airport.keys()))[0]
        dataEntry = mp.get(analyzer['airportsMap'], name)
        data = me.getValue(dataEntry)
        print(data)


def printResults5(result):

    print('El numero de aeropuertos afectados por el cierre es: ' + str(result[0]))
    print('Los aeropuertos afectados por el cierre son: ')
    print(result[1])


def printMenu():
    print("-----------------------------------------------------------------------------")
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexión aérea")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4- Encontrar la ruta más corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")
    print("7- Comparar con servicio WEB externo")
    print("8- Visualizar gráficamente los requerimientos")
    print("0- Cerrar aplicacion")
    print("-----------------------------------------------------------------------------")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        analyzer = controller.init()
        controller.loadData(analyzer)
        print('Para el grafo 1 hay: ')
        print(str(gr.numVertices(analyzer['airports'])) + ' aeropuertos')
        print(str(gr.numEdges(analyzer['airports'])) + ' rutas aereas con una direccion')
        print("Para el grafo 2 hay: ")
        print(str(gr.numVertices(analyzer['airportsB'])) + ' aeropuertos')
        print(str((gr.numEdges(analyzer['airportsB'])//2)) + ' rutas aereas en ambas direcciones')
        print('Para el grafo 3 de ciudades y aeropuertos hay: ')
        print(str(gr.numVertices(analyzer['graphCities'])) + ' aeropuertos y ciudades')
        print(str(gr.numEdges(analyzer['graphCities'])) + ' rutas aeropuerto-ciudad o viceversa')
        print('El total de ciudades es de: ' + str(mp.size(analyzer['cities'])))
        cities = mp.keySet(analyzer['cities'])
        cityl = lt.getElement(cities, (lt.size(cities) - 1))
        city1entry = mp.get(analyzer['cities'], cityl)
        print('La ultima ciudad cargada es ' + cityl + ' y sus datos asociados son: ')
        print(me.getValue(city1entry))
        airports = mp.keySet(analyzer['airportsMap'])
        airport1 = lt.getElement(airports, 1)
        airportsentry = mp.get(analyzer['airportsMap'], airport1)
        print('El primer aeropuerto cargado es ' + airport1 + ' y sus datos asociados son: ')
        print(me.getValue(airportsentry))

    elif int(inputs[0]) == 2:

        result = controller.interconexionPoints(analyzer)
        printResults1(analyzer, result)

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:

        city1 = input('Nombre de la ciudad de origen: ')
        city2 = input('Nombre de la ciudad de llegada: ')
        city1LstEntry = mp.get(analyzer['cities'], city1)
        city1Lst = me.getValue(city1LstEntry)
        city2LstEntry = mp.get(analyzer['cities'], city2)
        city2Lst = me.getValue(city2LstEntry)
        size1 = lt.size(city1Lst)
        if size1 > 1:
            for element in lt.iterator(city1Lst):
                print(element)
            n = int(input('Dadas las ciudades en orden, digite el numero de la ciudad de origen que desea buscar (1 o 2 o 3... o n): '))
            city1f = lt.getElement(city1Lst, n)
        else:
            city1f = city1

        size2 = lt.size(city2Lst)
        if size2 > 1:
            for element in lt.iterator(city2Lst):
                print(element)
            n = int(input('Dadas las ciudades en orden, digite el numero de la ciudad de llegada que desea buscar (1 o 2 o 3... o n): '))
            city2f = lt.getElement(city2Lst, n)
        else:
            city2f = city2

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:

        airport = input('Codigo IATA del aeropierto a cerrar: ')
        result = controller.affectedAirports(analyzer, airport)
        printResults5(result)

    elif int(inputs[0]) == 7:
        pass

    elif int(inputs[0]) == 8:
        pass

    else:
        sys.exit(0)
sys.exit(0)
