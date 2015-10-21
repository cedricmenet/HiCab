# -*- coding: utf-8 -*-
import json, copy, random
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
    json_map = add_infos_on_map(json_map)
    return json_map

def get_coord(location, json_map):
    if location['loc_type'] == "street":
        return get_coord_on_street(location, json_map)
    elif location['loc_type'] == "bridge":
        return get_coord_on_bridge(location, json_map)
    return None

def get_coord_on_bridge(bridge, json_map):
    coord = {}
    if not bridge == None:
        area = get_area(bridge['area'], json_map['areas'])
        vertex = get_vertex(bridge['from'], area['map'])
        coord['x'] = vertex["x"]
        coord['y'] = vertex["y"]
    return coord
    
def get_coord_on_street(street, json_map):
    coord = {}
    if not street == None:
        backward = False
        if "backward" in street:
            backward = street['backward']
        vertex_a = None
        vertex_b = None
        area = get_area(street['area'], json_map['areas'])
        progress = street['progression']
        if not backward:
            vertex_a = get_vertex(street['path'][0], area['map'])
            vertex_b = get_vertex(street['path'][1], area['map'])
        else:
            vertex_a = get_vertex(street['path'][1], area['map'])
            vertex_b = get_vertex(street['path'][0], area['map'])
        # Made in Feth
        #coord['x'] = (1.0 - progress) * vertex_a["x"] + progress * vertex_b["x"]
        #coord['y'] = (1.0 - progress) * vertex_a["y"] + progress * vertex_b["y"]
        # Made in Cedric
        coord['x'] = vertex_a["x"] + progress * (vertex_b["x"] - vertex_a["x"])
        coord['y'] = vertex_a["y"] + progress * (vertex_b["y"] - vertex_a["y"])
    return coord

# Ajout de la pondération et le nom des area sur les rues et les bridges
def add_infos_on_map(json_map):
    for area in json_map['areas']:
        for street in area['map']['streets']:
            vertex_a = get_vertex(street['path'][0], area['map'])
            vertex_b = get_vertex(street['path'][1], area['map'])
            street['weight'] =  get_weight(vertex_a, vertex_b)
            street['area'] = area['name']
            street['loc_type'] = "street"
        for bridge in area['map']['bridges']:
            bridge['area'] = area['name']
            bridge['name'] = "from:" + bridge['from'] + "_to:" + bridge['to']['vertex'] + "@" + bridge['to']['area']
            bridge['loc_type'] = "bridge"
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
        if vertex_name_a == street['path'][0] and vertex_name_b == street['path'][1]:
            new_street = copy.copy(street)
            new_street['backward'] = False
            return new_street
        elif not street['oneway'] and vertex_name_a == street['path'][1] and vertex_name_b == street['path'][0]:
            new_street = copy.copy(street)
            new_street['backward'] = True
            return new_street
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
    return sqrt(((vertex_a['x']-vertex_b['x'])*1.0)**2 + ((vertex_a['y']-vertex_b['y'])*1.0)**2)
    
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
    street = copy.copy(streets[random.randrange(len(streets))])
    street['progression'] = random.random()
    return street


# Obtient le chemin le plus court
def get_path(json_map, street_start, street_end):
    start_encode = street_start["path"][1] + "@" + street_start["area"]
    end_encode = street_end["path"][0] + "@" + street_end["area"]
    graph = get_graph(json_map)
    path_encode = dij_rec(graph,start_encode,end_encode)['path']
    path = []
    path.append(street_start)
    for i in range(len(path_encode) - 1):
        loc = convert_to_loc(json_map['areas'], path_encode[i], path_encode[i+1])
        path.append(loc)
    path.append(street_end)
    return path

## MAIN TEST
"""
json_map = load_map("map.json")
start = get_random_street(json_map)
stop = get_random_street(json_map)
print get_path(json_map, start, stop)
"""
