#region IMPORTS
import hashlib
import json
import monitoring
import os
import random
import secretary
import socket
import string
import threading
import time
#endregion

#region HTTP-CODES
HTTP_OK 				 = 200
HTTP_NO_CONTENT          = 204
HTTP_BAD_REQUEST 		 = 400
HTTP_FORBIDDEN 			 = 403
HTTP_NOT_FOUND 			 = 404
HTTP_NOT_ACCEPTABLE 	 = 406
HTTP_PRECONDITION_FAILED = 412
HTTP_EXPECTATION_FAILED  = 417
HTTP_LOCKED 			 = 423
HTTP_NOT_IMPLEMENTED 	 = 501
#endregion

# TARGETS
TARGET_CLOSET = 1

# GENERAL VARIABLES
PORT = 52323
VERSION = '1.0.2'

# THREADING VARIABLES
editing_handler = None
connected_ips = []
lock = threading.Lock()


def get_target_filename(target):
	if target == TARGET_CLOSET:
		return "closet.json"


class EditingThread(threading.Thread):
	def __init__(self, ip, target):
		super().__init__()
		self.ip = ip
		self.name = "Editing: " + ip
		self.target = target
		self.offline_seconds = 0
		self.running = True

	def is_ip_online(self):
		for ip in connected_ips:
			if ip == self.ip:
				return True
			else:
				return False

	def stop(self):
		global editing_handler; editing_handler = None
		self.running = False

	def run(self):
		while self.running:
			if not self.is_ip_online:
				if self.offline_seconds == 5 * 60:
					self.stop()
					continue
				time.sleep(1)
				self.offline_seconds += 1


class ClientTread(threading.Thread):

	log = secretary.LogEntry()

	def __init__(self, conn, ip):
		super().__init__()
		self.conn = conn
		self.conn.settimeout(2)
		self.name = ip
		self.ip = ip
		self.running = True
		monitoring.addConnection(ip)
		self.log.saveIP(ip)
		self.client_info = self.request_sign_up()

	# CONNECTION
	def request_sign_up(self):
		client_info = {}
		self.conn.settimeout(2)
		data = json.dumps(self.conn.recv(1024))
		
		# wrong request
		if data['action'] != 1:
			self.send({'action': data['action'], 'code': HTTP_NOT_ACCEPTABLE})
			return {}
		
		if self.resources_available('login_data.json'):
			with open('login_data.json', 'rb') as f:
				login_data = json.load(f.read())

			for role in login_data:
				if data['password'] == login_data[role]['key']:
					client_info['role_name'] = role
					client_info['password'] = login_data[role]['key']
					client_info['level'] = login_data[role]['level']
					break
			else:
				# wrong password
				self.send({'action': data['action'], 'code': HTTP_FORBIDDEN})
				return {}

		# check hash
		if self.resources_available(get_target_filename(TARGET_CLOSET)):
			with open(get_target_filename(TARGET_CLOSET), 'rb') as f:
				if not data['hash']['closet'] == hashlib.sha256(f.read()).hexdigest():
					client_info['latest_closet'] = False
				else: client_info['latest_closet'] = True
		else:
			self.send({'action': data['action'], 'code': HTTP_NOT_FOUND})
			return {}

		if editing_handler:
			if editing_handler.ip == self.ip:
				client_info['editing'] = 1
			else: client_info['editing'] = 0
		else: client_info['editing'] = 0

		self.send({'action': data['action'], 'code': HTTP_OK, 'roleName': client_info['role_name'], 'roleLevel': client_info['role_level'], 'editing': client_info['editing']})
		return client_info

	# ACTION
	def action_edit_target(self):
		pass

	def action_refresh_target(self, jdic):
		# check if required resources are available
		if not self.resources_available(get_target_filename(jdic['target'])):
			self.send({'data': {}, 'code': HTTP_NOT_FOUND, 'action': jdic['action']})
			return

		# actual function
		hasher = hashlib.sha256()
		with open(get_target_filename(jdic['target']), 'rb') as json_data:
			data = json.load(json_data.read())
			hasher.update(json_data.read())

		closet_hash = hasher.hexdigest()

		if closet_hash == jdic['hash']:
			self.send({'data': {}, 'code': HTTP_NO_CONTENT, 'action': jdic['action']})
		else:
			self.send({'data': data, 'code': HTTP_OK, 'action': jdic['action'], 'hash': closet_hash})

	# EDIT
	def handle_request_leave_editing(self, jdic):
		if editing_handler:
			if editing_handler.ip == self.ip:
				lock.acquire()
				self.edting_handler.stop()
				self.client_info['editing'] = 0
				lock.release()

	def handle_request_edit_target(self, jdic):
		global editing_handler

		# check if required resources are available
		if self.resources_available(get_target_filename(jdic['target'])):
			self.send({'action': jdic['action'], 'code': HTTP_NOT_FOUND})
			return
		
		if self.resources_available('login_data.json'):
			self.send({'action': jdic['action'], 'code': HTTP_NOT_FOUND})
			return

		# actual function
		with open('login_data.json') as json_data:
			login_data = json.load(json_data)

		for role in login_data:
			if role['key'] == jdic['key']:
				if role['level'] >= 2:
					hasher = hashlib.sha256()
					with open(get_target_filename(jdic['target']), 'rb') as closet:
						hasher.update(closet.read())
					
					if not editing_handler:
						if hasher.hexdigest() == jdic['hash']:
							lock.acquire() # blocking other clients so only one person can change the editing state
							edting_handler = EditingThread(self.ip, jdic["target"])
							edting_handler.start()
							self.send({'code': HTTP_OK, 'action': jdic['action']})
							lock.release()
						else: self.send({'action': jdic['action'], 'code': HTTP_PRECONDITION_FAILED})
					else:
						self.send({'action': jdic['action'], 'code': HTTP_LOCKED})
		else:
			self.send({'action': jdic['action'], 'code': HTTP_NOT_ACCEPTABLE})

	def handle_request_update_target(self, jdic):
		# TODO: safe target
		# check if required resources are available
		if self.resources_available(get_target_filename(jdic['target'])):
			self.send({'action': jdic['action'], 'code': HTTP_NOT_FOUND})
			return

		# actual function
		if editing_handler:
			if editing_handler.ip == self.ip:
				with open(get_target_filename(jdic['target']), 'w') as target_file:
					target_file.write(jdic['data'])
				
				hasher = hashlib.sha256(bytes(jdic['data']))

				self.send({'action': jdic['action'], 'code': HTTP_OK, 'hash': hasher.hexdigest()})
	
	# ------------------- #
	def resources_available(self, target):
		# check if required resources are available
		if not get_target_filename(target) in os.listdir(os.path.dirname(__file__)):
			return False
		return True

	def disconnect(self):
		self.running = False
		monitoring.removeConnection(self.name)
		connected_ips.remove(self.ip)

	def send(self, jdic):
		self.log.saveOutput(jdic)
		self.log.writeLog()
		self.conn.send(json.dumps(jdic).encode('utf8'))

	def run(self):
		# refresh closet
		if self.client_info['latest_closet'] == False:
			if self.resources_available(get_target_filename(TARGET_CLOSET)):
				with open(get_target_filename(TARGET_CLOSET), 'rb') as f:
					self.send({'action': 0, 'data': f.read()})

		while self.running:
			try:
				data = self.conn.recv(1024)
				# HANDLE 0 BYTES (Client disconnected)
				if data == b'':
					self.disconnect()
					continue
				data = json.loads(data)
				self.log.saveInput(data)
				
				# HANDLE DATA
				if data['request'] == 1:
					self.handle_request_validate_password(data)
				elif data['request'] == 2:
					self.handle_request_extend_edit_closet(data)
				elif data['request'] == 3:
					self.handle_request_leave_editing()
				elif data['request'] == 10:
					self.handle_request_refresh_closet(data)
				elif data['request'] == 11:
					self.handle_request_edit_closet(data)
				elif data['request'] == 12:
					self.handle_request_update_closet(data)
				else:
					self.send({'data': {}, 'code': HTTP_NOT_IMPLEMENTED, 'request': data['request']})
			
			# HANDLE EXCEPTIONS
			except ConnectionResetError:
				self.disconnect()
			except ConnectionAbortedError:
				self.disconnect()
				'''except KeyError:
				self.send({'data': {}, 'code': HTTP_BAD_REQUEST, 'request': -1})'''
			except json.decoder.JSONDecodeError:
				self.send({'data': {}, 'code': HTTP_BAD_REQUEST, 'request': -1})
				'''except Exception as e:
				self.send({'data': {}, 'code': HTTP_BAD_REQUEST, 'request': -1})
				self.running = False'''

		self.conn.close()


def main():
	# Server Setup
	monitoring.saveVersion(VERSION)
	monitoring.saveExecutionInterval(60)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Server läuft übers internet (TCP)
	server.bind(("", PORT)) # Auf der ip vom Rechner, auf dem das Programm ausgeführt wird auf dem Port 52323
	server.listen(10) # Es können maximal 10 Clients gleichzeitig verbunden sein

	while True:
		monitoring.timeExecution()
		try:
			conn, addr = server.accept() # Akzeptiert Verbindungen
			connected_ips.append(addr[0])
			ClientTread(conn, addr[0]).start() # Ein neuer Thread wird gestartet, der das Speichern der Datei übernimmt
		except socket.timeout:
			pass
		except KeyboardInterrupt:
			break


	server.close()

main()
