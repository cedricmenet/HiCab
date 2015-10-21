# -*- coding: utf-8 -*-
import time
import json
from threading import Thread, Lock
from map_manager import *

# Représente un taxi
class Cab(object):
	def __init__(self, id_cab, json_map):
		self.id_cab = id_cab
		self.position = get_random_street(json_map)
		self.odometer = 0
		self.is_busy = False
		self.current_request = None
		self.has_changed = False
		self.path = []
		self.json_map = json_map

	# Permet d'accepter ou refuser une requête
	def handle_request(self,requests_queue, accepted):
		if not self.is_busy:
			if accepted:
				# Accepte la première requête de la file
				self.current_request = requests_queue[0]
				self.is_busy = True
				self.odometer = 0
				self.path = get_path(self.json_map, self.position, self.current_request.location)
				print('[.. CabDevice#'+ str(self.id_cab) +']: Accept a cab request')
			else:
				print('[.. CabDevice#'+ str(self.id_cab) +']: Refuse a cab request')
			# On retire la requête de la liste
			requests_queue.remove(requests_queue[0])
			self.has_changed = True
	
	# Observe si des changements sont apportés à l'instance et set la propriété "has_changed"
	def __setattr__(self, name, value):
		if (not hasattr(self, name) or getattr(self, name) != value) and name != "has_changed":
			self.has_changed = True
		super(Cab, self).__setattr__(name, value)

	# Avance le taxi en suivant le path, et s'arrête si il arrive au client
	def move_forward(self):
		if self.is_busy:
			self.odometer += 0.1
			traffic_jam = self.position["weight"]
			progress = 0.01 / traffic_jam
			total_progress = self.position["progression"] + progress
			is_arrived = False
			# Gestion de l'arrêt au client
			if self.position["name"] == self.current_request.location["name"]:
				destination = self.current_request.location
				if "progression" in destination and total_progress >= destination["progression"]:
					self.is_busy = False
					self.position["progression"] = destination["progression"]
					self.current_request = None
					is_arrived = True
					print('[.. CabDevice#'+ str(self.id_cab) +']: $$ Mission complete $$')
			if not is_arrived:
				# Gestion du suivi de chemin
				if total_progress < 1:
					self.position["progression"] += progress
				else:
					# Changement de location
					if len(self.path) > 0:
						self.path = self.path[1:]
						self.position = self.path[0]
						self.position["progression"] = total_progress - 1
					else:
						# Pas de chemin à suivre 
						self.position["progression"] = 1
						self.is_busy = False
						print('[.. CabDevice#'+ str(self.id_cab) +']: Where should i go ?')

# Représente une demande de taxi
class CabRequest(object):
	def __init__(self, id_request, location):
		# Id de la requête
		self.id_request = id_request
		# Localisation de la requête
		self.location = location
		# Défini si la requête est nouvelle
		self.is_new = True

# Monitor l'ensemble des cabs, permettant une communication avec les devices associés
class CabMonitoring(Thread):
	def __init__(self, cabs, requests, cab_channels, display_channels, cab_lock, request_lock):
		# Nécessaire pour les Threads
		Thread.__init__(self)
		# Liste des cabs managé
		self.cabs = cabs
		# File d'attente des requêtes
		self.requests_queue = requests
		# Channels de communication avec les cab_device
		self.cab_channels = cab_channels
		# Channels de communication avec les display_device
		self.display_channels = display_channels
		# Indique si le monitoring doit être actif ou pas
		self.on_air = True
		# Thread Lockers
		self.cab_lock = cab_lock
		self.request_lock = request_lock
	
	# Thread permettant l'envoi vers les channels si des modifications ont eu lieu
	def run(self):
		print("[.. Monitoring] Start")
		self.on_air = True
		while self.on_air:
			# Verrouillage des lockers
			self.cab_lock.acquire()
			self.request_lock.acquire()
			# Vérification des changements dans la requests_queue
			queue_changed = False
			for request in self.requests_queue:
				if request.is_new:
					queue_changed = True
					request.is_new = False
			# Vérification des changements dans les cabs et envoi au cab_device
			cabs_changed = False
			for cab in self.cabs:
				if cab.has_changed or queue_changed:
					self.send_to_cabs(cab)
					cabs_changed = cabs_changed or cab.has_changed
					cab.has_changed = False
			# Envoi aux displays si changement détecté sur les cabs
			if cabs_changed:
				self.send_to_displays()
			# Deverouillage des lockers
			self.cab_lock.release()
			self.request_lock.release()
			# Temporisation 
			time.sleep(0.15)
	
	# Arrêt du thread de monitoring
	def stop_monitoring(self):
		print("[.. Monitoring] Stop")
		self.on_air = False
	
	# Envoi des infos vers les cab_device inscrits
	def send_to_cabs(self, cab):
		# Construction du message
		message = str({"id_cab":cab.id_cab,
					   "odometer":cab.odometer,
					   "is_busy":cab.is_busy,
					   "queue":len(self.requests_queue)})
		# Envoi sur les cab_channels associés
		for channel in self.cab_channels:
			if channel.cab.id_cab == cab.id_cab:
				channel.send(message)
		
	# Envoi des infos vers les display_device inscrits
	def send_to_displays(self):
		# Construction du message
		message = {}
		message['cab_infos'] = []
		for cab in self.cabs:
			cab.position["coord"] = get_coord(cab.position, cab.json_map)
			new_info = {"id_cab":cab.id_cab,
						"location":cab.position}
			message['cab_infos'].append(new_info)
		# Envoi sur les display_channels associés
		for channel in self.display_channels:
			channel.send(json.dumps(message))

# Channel de communication avec les cab_device
class ChannelCab:
	def __init__(self, cab, requests_queue, ws, cab_lock, request_lock):
		self.cab = cab
		self.requests_queue = requests_queue
		self.websocket = ws
		self.on_air	= True
		self.cab_lock = cab_lock
		self.request_lock = request_lock
	
	# Ecoute des messages du cab_device
	def listen(self):
		while self.on_air:
			try:
				message = self.websocket.receive()
				print('[<= CabDevice#'+ str(self.cab.id_cab) +']: ' + message)
			except:
				print('[XX CabDevice#'+ str(self.cab.id_cab) +']: Listener connection lost')
				self.on_air = False
			if len(self.requests_queue) > 0:
				self.cab_lock.acquire()
				self.request_lock.acquire()
				try:
					self.cab.handle_request(self.requests_queue, json.loads(message)['is_accepted'])
				except:
					print('[.. CabDevice#'+ str(self.cab.id_cab) +']: Invalid message')
				self.cab_lock.release()
				self.request_lock.release()
	
	# Envoi de message vers le cab_device
	def send(self, message):
		if self.on_air:
			print('[=> CabDevice#'+ str(self.cab.id_cab) +']: ' + message)
			try:
				self.websocket.send(message)
			except:
				print('[XX CabDevice#'+ str(self.cab.id_cab) +']: Transmitter connection lost')
				self.on_air = False

# Channel de communication avec les display_device
class ChannelDisplay:
	def __init__(self, json_map, requests_queue, ws, request_lock):
		self.requests_queue = requests_queue
		self.websocket = ws
		self.on_air = True
		self.request_lock = request_lock
		self.json_map = json_map
		
	# Ecoute des messages du display_device
	def listen(self):
		while self.on_air:
			try:
				message = self.websocket.receive()
				print('[<= DisplayDevice]: ' + message)
			except:
				print('[XX DisplayDevice]: Listener connection lost')
				self.on_air = False
			self.request_lock.acquire()
			try:
				new_req = CabRequest(len(self.requests_queue), json.loads(message)['location'])
				if not "name" in new_req.location:
					new_req.location = get_random_street(self.json_map)
					print('[.. DisplayDevice]: Random request generated : ' + str(new_req.location))
				self.requests_queue.append(new_req)
				print('[.. DisplayDevice]: New request registered')
			except:
				print('[.. DisplayDevice]: Invalid message')
			self.request_lock.release()
	
	# Envoi de message vers le display_device
	def send(self, message):
		if self.on_air:
			print("[=> DisplayDevice]: " + message)
			try:
				self.websocket.send(message)
			except:
				print('[XX DisplayDevice]: Transmitter connection lost')
				self.on_air = False