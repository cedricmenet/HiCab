# -*- coding: utf-8 -*-
import json

def get_data_from_json(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data
    
def get_graph(json_map):
    g = { 'm#0' : {'b#0': 1.2} }
    return g
    
def get_weight(vertex_a, vertex_b):
    
    
    
## MAIN TEST
json_map = get_data_from_json('map.json')
print(json_map)
graph = get_graph(json_map)
print("")
print("graph = " + str(graph))