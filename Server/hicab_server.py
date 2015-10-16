# -*- coding: utf-8 -*-

#from gevent import monkey
#monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request, jsonify, send_from_directory
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect

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
socketio = SocketIO(app)

####### FONCTIONS #######
# Thread de déplacement des cabs
def cabs_move_thread():
	while True:
		time.sleep(5)
		count += 1
		socketio.emit('my response',
					{'data': 'Server generated event', 'count': count},
					namespace='/test')

####### WEBSERVER #######
# Page d'accueil
@app.route('/')
def index():
	#global thread
	#if thread is None:
		#thread = Thread(target=cabs_move_thread)
		#thread.start()
	return render_template('index.html')
	
# Page de test des WebSockets
@app.route('/test/websocket')
def test_websocket():
	return render_template('test_websocket.html')
	
####### WEBSERVICES #######
# Renvoie les scripts JS
@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

# Renvoie le JSON contenant la description des maps
@app.route('/api/getmap')
def get_map():
	return jsonify({'areas':areas})

# Renvoie les informations nécessaire pour la connection WebSocket
@app.route('/api/getsocket')
def get_socket():
	device_type = request.args.get('device_type', '')
	response = {'host': u'192.168.1.1', 'port': 80, 'room': u'default_room', 'device_id' : 0}
	if device_type == 'cab_device':
		new_cab = Cab(len(cabs), None)
		cabs.append(new_cab)
		response['room'] = 'cab_device'
		response['device_id'] = new_cab.id_cab
	elif device_type == 'display':
		response['room'] = 'display'
	return jsonify(response)

####### WEBSOCKET #######

#### RECEPTION 
# Inscription à une room
@socketio.on('subscribe')
def subscribe_room(message):
	join_room(message['room'])
	print('Room subscribed: ' + message['room'])

# Reception des messages des clients
@socketio.on('publish')
def receive_message(message):
	if (message['type'] == 'request'):
		# Nouvelle requête reçue: ajout dans la liste
		request = message['data']
		new_request = CabRequest(len(requests), request['localisation'])
		requests.append(new_request)
		# Préparation du message requests_queue
		data = []
		for req in requests:
			data.append({'id_request': req.id_request,
				 		 'cabs_responses' : req.cabs_responses})
		msg_queue = {'type': u'requests_queue', 
					 'requests': data}
		# Envoi de la nouvelle queue dans la room cab_device
		send_room_message(msg_queue, 'cab_device')
	elif (message['type'] == 'request_response'):
		toto = None
	print('Message published: ' + message['data'])

# Désinscription à une room
@socketio.on('unsubscribe')
def leave(message):
	leave_room(message['room'])
	print('Room unsubscribed: ' + message['room'])

# Déconnection d'un client
@socketio.on('user_disconnecting')
def disconnect_request():
	disconnect()
	print('Client disconnected')

# Connection d'un client => useless ??
@socketio.on('user_connecting')
def connect_request():
	print('Client connected')

#### EMISSION
# Envoi d'un message dans une room (depuis la page de test)
@socketio.on('send_room_message')
def send_room_message(message):
	emit('receive',
		{'type': message['type'], 'room': message['room'] ,'data': message['data']},
		room = message['room'])
	print('Message emit on room: ' + message['room'] + ', data:' + message['data'])

# Envoi d'un message dans une room
def send_room_message(message, room_name):
	emit('receive',	jsonify(message), room = room_name)
	print('Message emit on room: ' + room_name + ', data: ' + message)


####### MAIN #######
if __name__ == '__main__':
	socketio.run(app, host="0.0.0.0", port=80)