import folium
from math import radians, sin, cos, sqrt, atan2
import itertools

# Fórmula de Haversine para calcular distancias entre dos puntos geográficos
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en kilómetros
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Coordenadas actualizadas de las ciudades principales en Ecuador
cities_coords = {
    "Quito": (-0.22985, -78.52495),
    "Guayaquil": (-2.19616, -79.88621),
    "Cuenca": (-3.99313, -79.20422),
    "Loja": (-3.99313, -79.20422),
    "Machala": (-3.25861, -79.96053),
    "Manta": (-0.94937, -80.73137),
    "Durán": (-2.1688548, -79.8340647),
    "Esmeraldas": (0.9592, -79.65397),
    "Ambato": (-1.24908, -78.61675),
    "Santo Domingo": (-0.25305, -79.17536)
}

# Crear la matriz de distancias
distance_matrix = {}
for city1, (lat1, lon1) in cities_coords.items():
    distance_matrix[city1] = {}
    for city2, (lat2, lon2) in cities_coords.items():
        if city1 != city2:
            distance_matrix[city1][city2] = haversine(lat1, lon1, lat2, lon2)
        else:
            distance_matrix[city1][city2] = 0

# Algoritmo de fuerza bruta para resolver el TSP
def tsp_bruteforce(distance_matrix):
    cities = list(distance_matrix.keys())
    shortest_path = None
    min_distance = float('inf')
    
    for perm in itertools.permutations(cities):
        current_distance = 0
        for i in range(len(perm) - 1):
            current_distance += distance_matrix[perm[i]][perm[i + 1]]
        current_distance += distance_matrix[perm[-1]][perm[0]]  # Volver al punto de origen
        
        if current_distance < min_distance:
            min_distance = current_distance
            shortest_path = perm
    
    return shortest_path, min_distance

# Obtener el camino más corto y su distancia
shortest_path, min_distance = tsp_bruteforce(distance_matrix)

# Crear un mapa centrado en la ubicación media de las ciudades
map_center = [sum(lat for lat, lon in cities_coords.values()) / len(cities_coords),
              sum(lon for lat, lon in cities_coords.values()) / len(cities_coords)]

mymap = folium.Map(location=map_center, zoom_start=6)

# Añadir marcadores para las ciudades con coordenadas en el popup
for city, (lat, lon) in cities_coords.items():
    popup_text = f"{city}<br>Latitud: {lat}<br>Longitud: {lon}"
    folium.Marker([lat, lon], popup=popup_text).add_to(mymap)

# Añadir la ruta más corta al mapa
route_coords = [cities_coords[city] for city in shortest_path] + [cities_coords[shortest_path[0]]]
folium.PolyLine(route_coords, color='blue', weight=2.5, opacity=1).add_to(mymap)

# Guardar el mapa en un archivo HTML
mymap.save("tsp_solution_map.html")

# Imprimir resultados detallados
print("Informe detallado del Problema del Vendedor Viajero (TSP):\n")
print("Matriz de distancias entre ciudades:")
for city_from in cities_coords.keys():
    for city_to in cities_coords.keys():
        if city_from != city_to:
            print(f"Distancia entre {city_from} y {city_to}: {distance_matrix[city_from][city_to]:.2f} km")
    print()

print("Camino más corto con distancias entre ciudades:")
total_distance = 0
for i in range(len(shortest_path)):
    city_from = shortest_path[i]
    city_to = shortest_path[(i + 1) % len(shortest_path)]
    distance = distance_matrix[city_from][city_to]
    total_distance += distance
    print(f"{city_from} -> {city_to}: {distance:.2f} km")
print(f"Distancia total mínima: {total_distance:.2f} km")

print("\nRuta más corta:")
for city in shortest_path:
    print(f"{city} ->", end=" ")
print(shortest_path[0])

print("Mapa guardado como 'tsp_solution_map.html'")
