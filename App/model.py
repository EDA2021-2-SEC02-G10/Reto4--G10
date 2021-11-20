"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newAnalyzer():

    analyzer = {'airports': None,
                'airportsB': None,
                'cities': None
                }

    analyzer['airports'] = gr.newGraph(datastructure='ADJ_LIST',
                                       directed=True,
                                       size=14000,
                                       comparefunction=compareAirports)

    analyzer['airportsB'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=14000,
                                        comparefunction=compareAirportsB)

    analyzer['cities'] = gr.newGraph(datastructure='ADJ_LIST',
                                     directed=False,
                                     size=14000,
                                     comparefunction=compareCities)

    analyzer['check'] = mp.newMap(1400,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareA)

    return analyzer


# Funciones para agregar informacion al catalogo


def addAirport(analyzer, airport):

    if not gr.containsVertex(analyzer['airports'], airport):
        gr.insertVertex(analyzer['airports'], airport)
    return analyzer


def addConection(analyzer, air1, air2, distance):

    edge = gr.getEdge(analyzer['airports'], air1, air2)
    if edge is None:
        gr.addEdge(analyzer['airports'], air1, air2, distance)

    return analyzer


def addAirportB(analyzer, airport):

    if not gr.containsVertex(analyzer['airportsB'], airport):
        gr.insertVertex(analyzer['airportsB'], airport)
    return analyzer


def addConectionB(analyzer, air1, air2, distance):

    edge = gr.getEdge(analyzer['airportsB'], air1, air2)
    if edge is None:
        gr.addEdge(analyzer['airportsB'], air1, air2, distance)

    return analyzer

# Carga de vertices, arco y peso en el grafo airports


def loadRoutes(analyzer, airline, departure, destination, distance):
    """
    Formato de aeropuertos: IATA-Airport
    Ejemplo: 2B-AER y 2B-KZN, para la primera fila en routes_full
    """
    air1 = airline + ":" + departure
    air2 = airline + ":" + destination
    #addAirport(analyzer, departure)
    #addAirport(analyzer, destination)
    #addConection(analyzer, departure, destination, distance)
    addAirport(analyzer, air1)
    addAirport(analyzer, air2)
    addConection(analyzer, air1, air2, distance)
    #addConection(analyzer, air1, departure, 0)
    #addConection(analyzer, departure, air1, 0)
    #addConection(analyzer, air2, departure, 0)
    #addConection(analyzer, departure, air2, 0)

    # Se agregan los checks a la tabla de hash para crear el mapa de ambas direcciones
    check1 = departure + "-" + destination
    check2 = destination + "-" + departure

    if mp.contains(analyzer['check'], check2):
        entry = mp.get(analyzer['check'], check2)
        value = me.getValue(entry)
        lt.removeLast(value)
        lt.addLast(value, 1)
    else:
        if mp.contains(analyzer['check'], check1) is False:
            lst = lt.newList('ARRAY_LIST')
            lt.addLast(lst, distance)
            lt.addLast(lst, 0)
            mp.put(analyzer['check'], check1, lst)

    return analyzer


def fillAirportsB(analyzer):

    airports = mp.keySet(analyzer['check'])
    for airport in lt.iterator(airports):
        entry = mp.get(analyzer['check'], airport)
        value = me.getValue(entry)
        if lt.getElement(value, 2) == 1:
            dd = list(airport.split('-'))
            departure = dd[0]
            destination = dd[1]
            addAirportB(analyzer, departure)
            addAirportB(analyzer, destination)
            addConectionB(analyzer, departure, destination, lt.getElement(value, 1))

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista


def compareAirports(airport, keyvalueairport):

    aircode = keyvalueairport['key']
    if (airport == aircode):
        return 0
    elif (airport > aircode):
        return 1
    else:
        return -1


def compareAirportsB(airport, keyvalueairport):

    aircode = keyvalueairport['key']
    if (airport == aircode):
        return 0
    elif (airport > aircode):
        return 1
    else:
        return -1


def compareCities(airport, keyvalueairport):

    aircode = keyvalueairport['key']
    if (airport == aircode):
        return 0
    elif (airport > aircode):
        return 1
    else:
        return -1


def compareA(keyname, department):
    depEntry = me.getKey(department)
    if (keyname == depEntry):
        return 0
    elif (keyname > depEntry):
        return 1
    else:
        return -1


# Funciones de ordenamiento

