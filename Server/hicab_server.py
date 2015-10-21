# -*- coding: utf-8 -*-
import time
import json
from threading import Thread, Lock
from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_sockets import Sockets
from cab_manager import *
from map_manager import load_map

######## THREAD LOCKS #######
cab_lock = Lock()
request_lock = Lock()

######## VARIABLES #######
# Map
json_map = load_map('map.json')

# Liste de Cab
cabs = []
# Liste des CabRequest
requests = []

#Liste des channel
cab_channels = []
display_channels = []

# Demarrage du monitoring
thread_monitor = CabMonitoring(cabs, requests, cab_channels, display_channels, cab_lock, request_lock)
thread_monitor.start()
	
# Initialisation de Flask
app = Flask(__name__, static_url_path='')
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
sockets = Sockets(app)

def cabs_move_thread():
	while True:
		time.sleep(1)
		cab_lock.acquire()
		for cab in cabs:
			if cab.is_busy:
				cab.move_forward()
		cab_lock.release()
		
# Thread de déplacement
thread_move = None
thread_move = Thread(target=cabs_move_thread)
thread_move.start()


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

# Renvoie les CSS
@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css', path)

# Index
@app.route('/')
def send_index():
	return render_template('index.html')

# Renvoi la map
@app.route('/getmap')
def get_map():
	return jsonify(json_map)
	
# Inscription d'un taxis
@app.route('/subscribe/cab')
def subscribe_cab():
	cab_lock.acquire()
	new_cab = Cab(len(cabs), json_map)
	cabs.append(new_cab)
	response = {'id_cab': new_cab.id_cab,
				'channel': u'cab_device' }
	cab_lock.release()
	print ('[<= Subscribe] Cab #' + str(new_cab.id_cab) + ' registered')
	return jsonify(response)
	
# Inscription d'un nouvel afficheur
@app.route('/subscribe/display')
def subscribe_display():
	response = {'channel': u'display_device'}
	print ('[<= Subscribe] New display registered')
	return jsonify(response)

####### WEBSOCKET #######
# Gestion des channels cab_device
@sockets.route('/cab_device')
def channel_cab_device(ws):
	print("[<= CabDevice]: New cab connected")
	is_open = True
	cab = None
	# Récupération de l'ID du cab sur un 1er échange
	try:
		message = ws.receive()
		print('[<= CabDevice] Starting channel with: ' + message)
		id_cab = int(json.loads(message)['id_cab'])
		cab = cabs[id_cab]
	except:
		print('[XX CabDevice] Error: Invalid "id_cab" received')
		is_open = False
	if is_open:
		# Création du channel
		channel = ChannelCab(cab, requests, ws, cab_lock, request_lock)
		cab_channels.append(channel)
		# On marque le cab "changed" pour forcer un premier envoi par le monitor
		cab_lock.acquire()
		cab.has_changed = True
		cab_lock.release()
		# Mise en écoute du channel
		channel.listen()

# Gestion des channels display_device
@sockets.route('/display_device')
def channel_display_device(ws):
	print("[<= DisplayDevice]: New display connected")
	# Création du channel
	channel = ChannelDisplay(json_map, requests, ws, request_lock)
	display_channels.append(channel)
	# On marque les cabs "changed" pour forcer un premier envoi par le monitor
	cab_lock.acquire()
	for cab in cabs:
		cab.has_changed = True
	cab_lock.release()
	# Mise en écoute du channel
	channel.listen()
