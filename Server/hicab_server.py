# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request, jsonify, send_from_directory
from flask_sockets import Sockets

####### CLASSES #######
class Cab:
	def __init__(self, id_cab, position):
		self.id_cab = id_cab
		self.position = position
		self.destination = None
		self.odometer = 0
		
class CabRequest:
	def __init__(self, id_request):
		self.id_request = id_request
		self.cabs_responses = []
		self.localisation = None
		
class Localisation:
	def __init__(self):
		self.toto = None
	
######## VARIABLES #######
# Map
areas = [{'name': u'Quartier Nord','map': {'weight': {'w': 1,'h': 1},'vertices': [{'name': u'm','x': 0.5,'y': 0.5},{'name': u'b','x': 0.5,'y': 1}],'streets': [{'name': u'mb','path': [u'm',u'b'],'oneway': False}],'bridges': [{'from': u'b','to': {'area': u'Quartier Sud','vertex': u'h'},'weight': 2}]}},{'name': u'Quartier Sud','map': {'weight': {'w': 1,'h': 1},'vertices': [{'name': u'a','x': 1,'y': 1},{'name': u'm','x': 0,'y': 1},{'name': u'h','x': 0.5,'y': 0}],'streets': [{'name': u'ah','path': [u'a',u'h'],'oneway': False},{'name': u'mh','path': [u'm',u'h'],'oneway': False}],'bridges': [{'from': u'h','to': {'area': u'Quartier Nord','vertex': u'b'},'weight': 2}]}}]

# Liste de Cab
cabs = []

# Liste des CabRequest
requests = []

# Thread de déplacement
thread = None
	
# Initialisation de Flask
app = Flask(__name__, static_url_path='')
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
sockets = Sockets(app)

####### WEBSERVER #######
# Page de test des WebSockets
@app.route('/test/websocket')
def test_websocket():
	return render_template('test_websocket.html')
	
####### WEBSERVICES #######
# Renvoie les scripts JS
@app.route('/scripts/<path:path>')
def send_js(path):
	return send_from_directory('scripts', path)

####### WEBSOCKET #######

@sockets.route('/echo')
def echo_socket(ws):
	is_open = True
	while is_open:
		try:
			message = ws.receive()
			if message is not None:
				print('WEBSOCKET - - Echoed message: ' + message)
				ws.send(message)
		except:
			print('WEBSOCKET - - Connection closed')
			is_open = False