﻿"""
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


from DISClib.DataStructures.arraylist import size
from DISClib.DataStructures.chaininghashtable import contains
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import adjacents, containsVertex, gr, indegree, outdegree
from DISClib.Algorithms.Sorting import mergesort as ms
from math import radians, cos, sin, asin, sqrt
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

    analyzer['graphCities'] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=False,
                                          size=14000,
                                          comparefunction=compareCities)

    analyzer['check'] = mp.newMap(1400,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareA)

    analyzer['cities'] = mp.newMap(1400,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareA)

    analyzer['airportsMap'] = mp.newMap(1400,
                                        maptype='CHAINING',
                                        loadfactor=4.0,
                                        comparefunction=compareA)

    return analyzer


# Funciones para agregar informacion al catalogo


# Carga de vertices, arco y peso en el grafo airports


def loadRoutes(analyzer, airline, departure, destination, distance):
    """
    Formato de aeropuertos: IATA-Airport
    Ejemplo: 2B-AER y 2B-KZN, para la primera fila en routes_full
    """
    air1 = airline + ":" + departure
    air2 = airline + ":" + destination
    addAirport(analyzer, departure)
    addAirport(analyzer, destination)
    addConection(analyzer, departure, destination, distance)
    #addAirport(analyzer, air1)
    #addAirport(analyzer, air2)
    #addConection(analyzer, air1, air2, distance)
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

# Llena el mapa de ciudades


def loadCities(analyzer, city, lat, lng, country, n):

    if mp.contains(analyzer['cities'], city) is False:
        dictCity = {}
        lstCity = lt.newList('ARRAY_LIST')
        dictCity['city'] = city
        dictCity['lat'] = lat
        dictCity['lng'] = lng
        dictCity['country'] = country
        dictCity['id'] = n
        lt.addLast(lstCity, dictCity)
        mp.put(analyzer['cities'], city, lstCity)
    else:
        entry = mp.get(analyzer['cities'], city)
        lst = me.getValue(entry)
        dictCity = {}
        dictCity['city'] = city
        dictCity['lat'] = lat
        dictCity['lng'] = lng
        dictCity['country'] = country
        dictCity['id'] = n
        lt.addLast(lst, dictCity)


# Crea el 3er grafo a partir del archivo de aeropuertos y el mapa de cities

def loadAirports(analyzer, name, city, country, airport, lat, lng):

    # Se crea el mapa de airports para sacar la informacion
    if mp.contains(analyzer['airportsMap'], airport) is False:
        dictAir = {}
        lstAir = lt.newList('ARRAY_LIST')
        dictAir['name'] = name
        dictAir['city'] = city
        dictAir['country'] = country
        dictAir['airport'] = airport
        dictAir['lat'] = lat
        dictAir['lng'] = lng
        lt.addLast(lstAir, dictAir)
        mp.put(analyzer['airportsMap'], airport, dictAir)


    # Ahora se crea el grafo de graphCities

    cityDataEntry = mp.get(analyzer['cities'], city)
    if cityDataEntry is not None:
        cityDataLst = me.getValue(cityDataEntry)
        for element in lt.iterator(cityDataLst):
            if element['country'] == country:
                cityData = element
            else:
                cityData = lt.getElement(cityDataLst, 1)
        distance = haversine(lng, lat, cityData['lng'], cityData['lat'])
        addAirportC(analyzer, airport)
        addAirportC(analyzer, city)
        addConectionC(analyzer, airport, city, distance)
        addConectionC(analyzer, city, airport, distance)

"""
    # Se hacen las conexiones con otros aeropuertos

    if gr.containsVertex(analyzer['airports'], airport):
        lstAd = gr.adjacents(analyzer['airports'], airport)
        for element in lt.iterator(lstAd):
            edge = gr.getEdge(analyzer['airports'], airport, element)
            addConectionC(analyzer, airport, element, edge['weight'])
"""


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


def addAirportC(analyzer, vertex):

    if not gr.containsVertex(analyzer['graphCities'], vertex):
        gr.insertVertex(analyzer['graphCities'], vertex)
    return analyzer


def addConectionC(analyzer, ver1, ver2, distance):

    edge = gr.getEdge(analyzer['graphCities'], ver1, ver2)
    if edge is None:
        gr.addEdge(analyzer['graphCities'], ver1, ver2, distance)

    return analyzer


# Funciones de consulta


# REQ 1
def interconexionPoints(analyzer):

    # Grafo 1
    lst1 = lt.newList('ARRAY_LIST')
    for vertex in lt.iterator(gr.vertices(analyzer['airports'])):
        degree = indegree(analyzer['airports'], vertex) + outdegree(analyzer['airports'], vertex)
        temp = {}
        temp[vertex] = degree
        lt.addLast(lst1, temp)

    sorted_list1 = ms.sort(lst1, cmpVertexByDegree)
    topValueDict1 = lt.getElement(sorted_list1, 1)
    topValue1 = (list(topValueDict1.values()))[0]
    finalList1 = lt.newList('ARRAY_LIST')
    for i in range(1, 51):
        temp = lt.getElement(sorted_list1, i)
        value = (list(temp.values()))[0]
        if value == topValue1:
            lt.addLast(finalList1, temp)

    # Grafo 2
    lst2 = lt.newList('ARRAY_LIST')
    for vertex in lt.iterator(gr.vertices(analyzer['airportsB'])):
        degree = (gr.degree(analyzer['airportsB'], vertex))//2
        temp = {}
        temp[vertex] = degree
        lt.addLast(lst2, temp)

    sorted_list2 = ms.sort(lst2, cmpVertexByDegree)
    topValueDict2 = lt.getElement(sorted_list2, 1)
    topValue2 = (list(topValueDict2.values()))[0]
    finalList2 = lt.newList('ARRAY_LIST')
    for i in range(1, 51):
        temp = lt.getElement(sorted_list2, i)
        value = (list(temp.values()))[0]
        if value == topValue2:
            lt.addLast(finalList2, temp)

    return finalList1, finalList2, topValue1, topValue2


# REQ 5
def affectedAirports(analyzer, airport):

    check = []
    stack = st.newStack('SINGLE_LINKED')
    inicial = gr.adjacents(analyzer['airports'], airport)
    final = lt.newList('ARRAY_LIST')
    counter = 0
    for element in lt.iterator(inicial):
        st.push(stack, element)
        check.append(element)

    while st.isEmpty(stack) is False:

        adj = None
        top = None
        top = st.pop(stack)
        lt.addLast(final, top)
        counter += 1
        adj = gr.adjacents(analyzer['airports'], top)
        for element in lt.iterator(adj):
            if element not in check:
                st.push(stack, element)
                check.append(element)

    return counter, final     


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


def cmpVertexByDegree(element1, element2):

    n1 = (list(element1.values()))[0]
    n2 = (list(element2.values()))[0]
    r = True
    if n1 > n2:
        r = True
    else:
        r = False

    return r


# Funciones de calculo


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

