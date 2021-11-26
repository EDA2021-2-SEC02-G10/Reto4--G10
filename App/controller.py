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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos

def loadData(analyzer):

    loadRoutes(analyzer)
    model.fillAirportsB(analyzer)
    loadCities(analyzer)
    loadAirports(analyzer)

    return analyzer


def loadRoutes(analyzer):

    routesfile = cf.data_dir + 'routes_full.csv'
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"))
    for row in input_file:
        model.loadRoutes(analyzer, row['Airline'], row['Departure'],
                         row['Destination'], float(row['distance_km']))

    return analyzer


def loadCities(analyzer):

    citiesfile = cf.data_dir + 'worldcities.csv'
    input_file = csv.DictReader(open(citiesfile, encoding="utf-8"))
    for row in input_file:
        model.loadCities(analyzer, row['city'], float(row['lat']),
                         float(row['lng']), row['country'], row['id'])

    return analyzer


def loadAirports(analyzer):

    airportsfile = cf.data_dir + 'airports_full.csv'
    input_file = csv.DictReader(open(airportsfile, encoding="utf-8"))
    for row in input_file:
        model.loadAirports(analyzer, row['Name'], row['City'], row['Country'], row['IATA'],
                           float(row['Latitude']), float(row['Longitude']))

    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def interconexionPoints(analyzer):

    return model.interconexionPoints(analyzer)


def affectedAirports(analyzer, airport):

    return model.affectedAirports(analyzer, airport)


def routecities(analyzer, city1, city2):

    return model.routeCities(analyzer, city1, city2)

