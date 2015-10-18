# -*- coding: utf-8 -*-
import time
import json
from threading import Thread, Lock
from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_sockets import Sockets

####### CLASSES #######
class Cab:
	def __init__(self, id_cab, position):
		self.id_cab = id_cab
		self.position = position
		self.destination = None
		self.odometer = 0
		self.is_busy = False
		
	def get_status(self):
		return str({'id_cab': self.id_cab,
				'odometer': self.odometer,
				'is_busy': self.is_busy})
		
class CabRequest:
	def __init__(self, id_request):
		self.id_request = id_request
		self.cabs_responses = []
		self.localisation = None
		
class Localisation:
	def __init__(self):
		self.toto = None

######## CHANNELS #######
## CAB DEVICE ##
class CabDeviceTransmitter(Thread):
	def __init__(self, cab, ws):
		Thread.__init__(self)
		self.cab = cab
		self.websocket = ws
		self.on_air = True
		
	def run(self):
		
		while self.on_air:
			try:
				time.sleep(2)
				status = self.cab.get_status()
				print('[=> CabDevice#'+ str(self.cab.id_cab) +']: ' + status)
				self.websocket.send(status)
			except:
				print('[XX CabDevice#'+ str(self.cab.id_cab) +']: Transmitter connection lost')
				self.on_air = False

class CabDeviceListener(Thread):
	def __init__(self, cab, ws):
		Thread.__init__(self)
		self.cab = cab
		self.websocket = ws
		self.on_air = True
	def run(self):
		while self.on_air:
			try:
				message = self.websocket.receive()
				print('[<= CabDevice#'+ str(self.cab.id_cab) +']: ' + message)
			except:
				print('[XX CabDevice#'+ str(self.cab.id_cab) +']: Listener connection lost')
				self.on_air = False

class CabDeviceChannel():
	def __init__(self, cab, ws):
		self.cab = cab
		self.websocket = ws
		self.on_air = True
	
	def diffuse_channel(self):
		thread_listener = CabDeviceListener(self.cab, self.websocket)
		thread_transmitter = CabDeviceTransmitter(self.cab, self.websocket)
		thread_listener.start()
		thread_transmitter.start()
		thread_listener.join()
		thread_transmitter.join()
	

######## THREAD LOCKS #######
cabs_lock = Lock()

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

####### BACKGROUND #######
# Thread de déplacement des cabs
def cabs_move_thread():
	while True:
		time.sleep(5)
		cabs_lock.acquire()
		for cab in cabs:
			cab.odometer += 1
		cabs_lock.release()

####### WEBSERVER #######
# Page de test des WebSockets
@app.route('/test/websocket')
def test_websocket():
	return render_template('test_websocket.html')
	
@app.route('/simulation')
def simulation():
	device_type = request.args.get('device_type', 'cab_device')
	return render_template('simulation_' + device_type + '.html')

####### WEBSERVICES #######
# Renvoie les scripts JS
@app.route('/scripts/<path:path>')
def send_js(path):
	return send_from_directory('scripts', path)

# Inscription d'un taxis
@app.route('/subscribe/cab')
def subscribe_cab():
	cabs_lock.acquire()
	new_cab = Cab(len(cabs), None)
	cabs.append(new_cab)
	response = {'id_cab': new_cab.id_cab,
				'channel': u'cab_device' }
	cabs_lock.release()
	print ('[!! Subscribe] Cab #' + str(new_cab.id_cab) + ' registered')
	return jsonify(response)
	
# Inscription d'un nouvel afficheur
@app.route('/subscribe/display')
def subscribe_display():
	response = {'channel': u'display_device'}
	print ('[!! Subscribe] New display registered')
	return jsonify(response)
	
# Demarrage de la simulation des taxis
@app.route('/simulation/start_move')
def move_cabs():
	global thread
	if thread is None:
		thread = Thread(target=cabs_move_thread)
		thread.start()
		print('[Simulation] Start move')
	return ''

####### WEBSOCKET #######
# Envoi les infos aux cab_device
@sockets.route('/cab_device')
def channel_cab_device(ws):
	is_open = True
	cab = None
	#on recupere l'ID du cab
	try:
		message = ws.receive()
		print('[!! CabDevice] Starting channel with: ' + message)
		id_cab = int(json.loads(message)['id_cab'])
		cab = cabs[id_cab]
	except:
		print('[XX CabDevice] Error: Invalid "id_cab" received')
		is_open = False
	if is_open:	
		channel = CabDeviceChannel(cab, ws)
		channel.diffuse_channel()


# Echo (pour test)
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
