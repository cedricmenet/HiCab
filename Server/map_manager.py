# -*- coding: utf-8 -*-
import json
import random
from math import sqrt
from dijkstra import *

# Charge un fichier
def get_data_from_file(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data
   
# Enregistre un fichier
def save_file(filename, data):
    with open(filename, "w") as data_file:
        data_file.write(data)
    
# Charge la map dans map.json
def load_map(filename):
    json_map = get_data_from_file(filename)
    json_map = add_weight_on_streets(json_map)
    return json_map

# Ajout de la pondération sur les rues
def add_weight_on_streets(json_map):
    for area in json_map['areas']:
        for street in area['map']['streets']:
            vertex_a = get_vertex(street['path'][0], area['map'])
            vertex_b = get_vertex(street['path'][1], area['map'])
            street['weight'] =  get_weight(vertex_a, vertex_b)
    return json_map
  
# Construction d'un graph pondéré
def get_graph(json_map):
    g={}
    for area in json_map['areas']:
        # Traitement des streets
        for street in area['map']['streets']:
            node_name = street['path'][0] + "@" + area['name']
            neighbour_name = street['path'][1] + "@" + area['name']
            vertex_a = get_vertex(street['path'][0], area['map'])
            vertex_b = get_vertex(street['path'][1], area['map'])
            weight = get_weight(vertex_a, vertex_b)
            if not node_name in g:
                g[node_name] = {}
            g[node_name][neighbour_name] = weight
            if not street['oneway']:
                if not neighbour_name in g:
                    g[neighbour_name] = {}
                g[neighbour_name][node_name] = weight
        # Traitement des bridges
        for bridge in area['map']['bridges']:
           node_name = bridge['from'] + "@" + area['name']
           neighbour_name = bridge['to']['vertex'] + "@" + bridge['to']['area']
           weight = bridge['weight']
           if not node_name in g:
                g[node_name] = {}
           g[node_name][neighbour_name] = weight
    return g
    
# Recupère un vertex en fonction du nom
def get_vertex(vertex_name, map_data):
    for vertex in map_data['vertices']:
        if vertex['name'] == vertex_name:
            return vertex
    return None
       
# Récupère une area en fonction du nom
def get_area(area_name, areas_data):
    for area in areas_data:
        if area['name'] == area_name:
            return area
    return None
    
# Récupère une street selon les noms des deux vertices
def get_street(vertex_name_a, vertex_name_b, map_data):
    for street in map_data['streets']:
        if vertex_name_a in street['path'] and vertex_name_b in street['path']:
            return street
    return None

# Récupère un pont 
def get_bridge(vertex_name_a, vertex_name_b, area_name_a, area_name_b, areas):
    area_a = get_area(area_name_a, areas)
    for bridge in area_a['map']['bridges']:
        if bridge['from'] == vertex_name_a and bridge['to']['area'] == area_name_b and bridge['to']['vertex'] == vertex_name_b:
            return bridge
    return None
        
# Calcul le poid entre deux vertices
def get_weight(vertex_a, vertex_b):
    return sqrt(vertex_a['x']**2 + vertex_a['x']**2)
    
# Renvoi le chemin réel entre 2 vertex "encodé"
def convert_to_loc(areas, start_encode, stop_encode):
    # Recupération des noms des vertex et area
    split = start_encode.split('@')
    vertex_name_a = split[0]
    area_name_a = split[1]
    split = stop_encode.split('@')
    vertex_name_b = split[0]
    area_name_b = split[1]
    if area_name_a == area_name_b:
        # Recherche de street
        map_data = get_area(area_name_a, areas)['map']
        return get_street(vertex_name_a, vertex_name_b, map_data)
    else:
        # Recherche de pont
        return get_bridge(vertex_name_a, vertex_name_b, area_name_a, area_name_b, areas)

# Obtient une position aléatoire sur la map
def get_random_street(json_map):
    areas = json_map['areas']
    streets = areas[random.randrange(len(areas))]['map']['streets']
    street = streets[random.randrange(len(streets))]
    street['progression'] = random.random()
    return street


# Obtient le chemin le plus court
def get_path(json_map, start, end):
    graph = get_graph(json_map)
    path_encode = dij_rec(graph,start,end)['path']
    path = []
    for i in range(len(path_encode) - 1):
        loc = convert_to_loc(json_map['areas'], path_encode[i], path_encode[i+1])
        path.append(loc)
    return path

## MAIN TEST
"""
json_map = load_map()
start = "a@Quartier Sud"
end = "m@Quartier Nord"
path = get_path(json_map, start, end)
print(path)
save_file("path.txt", str(path))
"""
json_map = load_map()
print get_random_street(json_map)