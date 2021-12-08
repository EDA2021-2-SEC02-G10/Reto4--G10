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


from DISClib.Algorithms.Graphs.scc import KosarajuSCC, stronglyConnected, connectedComponents
from DISClib.Algorithms.Graphs.prim import PrimMST, edgesMST,prim
from DISClib.DataStructures.arraylist import size
from DISClib.DataStructures.chaininghashtable import contains
import config as cf
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import map as mp
from DISClib.ADT import queue as q
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import adjacents, containsVertex, gr, indegree, outdegree,numVertices
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import dijsktra as dk
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.Algorithms.Graphs import dfs as dfs
from math import radians, cos, sin, asin, sqrt
import folium 
import webbrowser
from amadeus import Client, ResponseError
import amadeus
assert cf

amadeus = Client(
    client_id='LCmwDrZVpQGFwrn6mzzt9Qq2SolQAH6v',
    client_secret='kaPXJqapidulSOhq'
)

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

    addAirport(analyzer, departure)
    addAirport(analyzer, destination)
    addConection(analyzer, departure, destination, distance)

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
        dictCity['lat'] = float(lat)
        dictCity['lng'] = float(lng)
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
        dictAir['lat'] = float(lat)
        dictAir['lng'] = float(lng)
        lt.addLast(lstAir, dictAir)
        mp.put(analyzer['airportsMap'], airport, dictAir)
        addAirport(analyzer, airport)


    # Ahora se crea el grafo de graphCities
"""
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
    for i in range(1, 7):
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
    for i in range(1, 7):
        temp = lt.getElement(sorted_list2, i)
        value = (list(temp.values()))[0]
        if value == topValue2:
            lt.addLast(finalList2, temp)

    return finalList1, finalList2, topValue1, topValue2

#REQ 2

def Clusters (analyzer,codigo1,codigo2):
    Kosaraju = KosarajuSCC(analyzer['airports'])
    aeropuertos_fuertemente_conectados = stronglyConnected(Kosaraju,codigo1,codigo2)
    
    cantidad_fuertemente_conectados = connectedComponents(Kosaraju)
    
    return (aeropuertos_fuertemente_conectados,cantidad_fuertemente_conectados)

# REQ 3


def routeCities(analyzer, city1, city2):

    # Calculo del aeropuerto mas cercano a cada ciudad
    airports = gr.vertices(analyzer['airports'])
    distance1Min = 100000000000000000000000000000000
    distance2Min = 100000000000000000000000000000000
    minAirport1 = None
    minAirport2 = None
    for airport in lt.iterator(airports):
        airportEntry = mp.get(analyzer['airportsMap'], airport)
        airportData = me.getValue(airportEntry)
        distance1 = None
        distance2 = None
        distance1 = haversine(city1['lng'], city1['lat'], airportData['lng'], airportData['lat'])
        distance2 = haversine(city2['lng'], city2['lat'], airportData['lng'], airportData['lat'])
        if gr.degree(analyzer['airports'], airport) == 0:
            distance1 = 1000000000000000000000000000000000
            distance2 = 1000000000000000000000000000000000
        if distance1 < distance1Min:
            distance1Min = distance1
            minAirport1 = airport
        if distance2 < distance2Min:
            distance2Min = distance2
            minAirport2 = airport

    # Obtencion de la distancia del trayecto
    search = dk.Dijkstra(analyzer['airports'], minAirport1)
    path = dk.pathTo(search, minAirport2)

    return minAirport1, minAirport2, path, distance1Min, distance2Min, city1, city2

# REQ 4

def Millas_viajero(analyzer, ciudad, millas):

    airport = ciudad
    km = millas*1.60
    used = 0
    nodeTotal = 0
    costTotal = 0
    distances = {}
    search = pr.PrimMST(analyzer['airportsB'])
    mst = pr.prim(analyzer['airportsB'], search, ciudad)
    nodeLst = lt.newList('ARRAY_LIST')
    tablen = (mst['distTo'])
    table = tablen['table']
    for element in lt.iterator(table):
        if element['key'] is not None:
            lt.addLast(nodeLst, element['key'])
            distances[element['key']] = element['value']

    bs = dfs.DepthFirstSearch(analyzer['airportsB'], airport)
    maxPath = None
    maxLength = 0
    nodeTotal = lt.size(nodeLst)
    for node in lt.iterator(nodeLst):
        costTotal += distances[node]
        path = dfs.pathTo(bs, node)
        if path is not None:
            length = st.size(path)
            if length > maxLength:
                maxPath = path
                maxLength = length

    final = lt.newList('ARRAY_LIST')
    for element in lt.iterator(maxPath):
        if element is not None:
            used += 2*(distances[element])
            if used > km:
                pass
            else:
                lt.addLast(final, element)

    finalDistances = []
    for element in lt.iterator(final):
        finalDistances.append(distances[element])

    return final, finalDistances, nodeTotal, costTotal, maxPath, used

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


# REQ 6

def compareResults(analyzer, city1, city2):

    lat1 = city1['lat']
    lng1 = city1['lng']
    lat2 = city2['lat']
    lng2 = city2['lng']
    airport1raw = amadeus.reference_data.locations.airports.get(longitude=lng1, latitude=lat1)
    airport2raw = amadeus.reference_data.locations.airports.get(longitude=lng2, latitude=lat2)
    airport1 = (airport1raw.data)[1]['iataCode']
    airport2 = (airport2raw.data)[1]['iataCode']
    airport1DistanceData = [(airport1raw.data)[1]['geoCode']['latitude'], airport1raw.data[1]['geoCode']['longitude']]
    airport2DistanceData = [(airport2raw.data)[1]['geoCode']['latitude'], airport2raw.data[1]['geoCode']['longitude']]
    airport1Distance = haversine(lng1, lat1, airport1DistanceData[1], airport1DistanceData[0])
    airport2Distance = haversine(lng2, lat2, airport2DistanceData[1], airport2DistanceData[0])

    #Obtencion de la distancia del trayecto
    search = dk.Dijkstra(analyzer['airports'], airport1)
    path = dk.pathTo(search, airport2)

    return airport1, airport2, path, airport1Distance, airport2Distance

# REQ 7

def seeRequirements(analyzer, data1, data2, data3, data4, data5):

    # REQ 1
    lstReq1 = data1[0]
    myMap1 = folium.Map()
    for airport in lt.iterator(lstReq1):

        name = (list(airport.keys()))[0]
        airportDataEntry = mp.get(analyzer['airportsMap'], name)
        airportData = me.getValue(airportDataEntry)
        lat = airportData['lat']
        lng = airportData['lng']
        folium.Marker([lat, lng], popup='TopAirport').add_to(myMap1)

    myMap1.save("map1.html")
    webbrowser.open("map1.html")

    # REQ 2
    port1 = data2[0]
    port2 = data2[1]
    print(port1)
    myMap2 = folium.Map()
    port1Entry = mp.get(analyzer['airportsMap'], port1)
    port1Data = me.getValue(port1Entry)
    port2Entry = mp.get(analyzer['airportsMap'], port2)
    port2Data = me.getValue(port2Entry)
    lat21 = port1Data['lat']
    lng21 = port1Data['lng']
    lat22 = port2Data['lat']
    lng22 = port2Data['lng']
    folium.Marker([lat21, lng21], popup='Airport1').add_to(myMap2)
    folium.Marker([lat22, lng22], popup='Airport2').add_to(myMap2)
    myMap2.save("map2.html")
    webbrowser.open("map2.html")

    # REQ 3
    path = data3[2]
    city1 = data3[5]
    city2 = data3[6]
    check = []
    myMap3 = folium.Map()
    while st.isEmpty(path) is False:
        top = st.pop(path)
        top1 = top['vertexA']
        top1Entry = mp.get(analyzer['airportsMap'], top1)
        top1Data = me.getValue(top1Entry)
        top2 = top['vertexB']
        top2Entry = mp.get(analyzer['airportsMap'], top2)
        top2Data = me.getValue(top2Entry)
        lat1 = top1Data['lat']
        lng1 = top1Data['lng']
        lat2 = top2Data['lat']
        lng2 = top2Data['lng']
        if top1 not in check:
            folium.Marker([lat1, lng1], popup='Airport').add_to(myMap3)
            check.append(top1)
        if top2 not in check:
            folium.Marker([lat2, lng2], popup='Airport').add_to(myMap3)
            check.append(top1)

    folium.Marker([city1['lat'], city1['lng']], popup='City').add_to(myMap3)
    folium.Marker([city2['lat'], city2['lng']], popup='City').add_to(myMap3)
    myMap3.save("map3.html")
    webbrowser.open("map3.html")

    # REQ 5
    final = data5[1]
    myMap5 = folium.Map()
    for airport in lt.iterator(final):
        airportDataEntry = mp.get(analyzer['airportsMap'], airport)
        airportData = me.getValue(airportDataEntry)
        lat = airportData['lat']
        lng = airportData['lng']
        folium.Marker([lat, lng], popup='AffAirport').add_to(myMap5)

    myMap5.save("map5.html")
    webbrowser.open("map5.html")


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

