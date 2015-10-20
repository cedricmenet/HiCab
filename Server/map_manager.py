# -*- coding: utf-8 -*-
import json
from math import sqrt

def get_data_from_json(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data
    
def save_file(filename, data):
    with open(filename, "w") as data_file:
        data_file.write(data)
    
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
    
def get_vertex(vertex_name, map_data):
    for vertex in map_data['vertices']:
        if vertex['name'] == vertex_name:
            return vertex
    return None
                   
def get_weight(vertex_a, vertex_b):
    return sqrt(vertex_a['x']**2 + vertex_a['x']**2)
    

## MAIN TEST
json_map = get_data_from_json('map.json')
print(json_map)
graph = get_graph(json_map)
print("")
print("graph = " + str(graph))
save_file("graph.txt", str(graph))