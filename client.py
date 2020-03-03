import threading
import json
import file_manager
import encryptor
import constants
from socket import timeout

class ClientThread(threading.Thread):

	def __init__(self, conn, ip):
		super().__init__()
		self.conn = conn
		self.name = 'Client {}'.format(ip)
		self.ip = ip
		self.running = True
		self.permissions = []
		self.handler = Handler()
		self.decryptor = encryptor.Decryptor()
		self.sign_up()
	
	# ------------------- #
	def sign_up(self):
		self.conn.settimeout(1)
		data = self.receive()
		if data:
			self.os, self.encryptor, is_valide = self.handler.handle_sign_up(data, self.decryptor.getN())
			if not is_valide:
				self.disconnect()
		else:
			self.disconnect()


	def disconnect(self):
		self.running = False
		self.conn.close()



	def run(self):
		while self.running:
			for transmission in self.handler.pending_transmissions:
				self.send(transmission)
			self.handler.pending_transmissions.clear()

			data = self.receive()
			if data and 'action' in data:
				if data['action'] is constants.REQUEST_LOGIN:
					self.permissions = self.handler.handle_login(data, self.decryptor, self.permissions)

	def send(self, jdic):
		print("New transmission: " + str(jdic))
		self.conn.send((json.dumps(jdic) + '\n').encode('utf8'))

	def receive(self):
		try:
			data = self.conn.recv(1024) # Receive 1024 byte (or try at least)

			if data == b'': # HANDLE 0 BYTES (Client disconnected)
				self.disconnect()
				return None
			
			data = json.loads(data)
			print('Received Data: ' + str(data))
			return data
		# HANDLE EXCEPTIONS
		except timeout:
			pass
		except KeyError:
			self.send({'code': constants.HTTP_BAD_REQUEST, 'action': -1})
		except json.decoder.JSONDecodeError:
			print('decode error')
			self.send({'code': constants.HTTP_BAD_REQUEST, 'action': -1})
		except ConnectionResetError:
			self.disconnect()
		except ConnectionAbortedError:
			self.disconnect()
		'''
		except Exception:
			print('unknown exception')
			self.send({'code': HTTP_BAD_REQUEST, 'action': -1})
			self.disconnect()
		'''
		return None
		
		
def has_keys(dict, keys):
	for key in keys:
		if not key in dict:
			return False
	return True

class Handler(object):

	def __init__(self):
		self.pending_transmissions = []

	def handle_sign_up(self, request, N):
		if has_keys(request, ['action','os', 'version', 'N', 'hash']) and request['action'] is constants.REQUEST_SIGN_UP: # Validate the request
			self.pending_transmissions.append({'action' : constants.REQUEST_SIGN_UP, 'code' : constants.HTTP_OK, 'N' : N})
			os = request['os']
			encrypt = encryptor.Encryptor(request['N'])
			hashes = request['hash']
			if 'creators' not in hashes or file_manager.has_changed(hashes['creators'], constants.TARGET_FILE_CREATORS):
				self.build_file_change_inform(constants.TARGET_FILE_CREATORS)

			if 'dates' not in hashes or file_manager.has_changed(hashes['dates'], constants.TARGET_FILE_DATES):
				self.build_file_change_inform(constants.TARGET_FILE_DATES)
			return os, encrypt, True # Return the client info

		self.pending_transmissions.append({'action' : constants.REQUEST_SIGN_UP, 'code' : constants.HTTP_BAD_REQUEST})
		return None, None, False

	def handle_login(self, request, decryptor, permissions):
		if 'keys' in request:
			for key in request['keys']:
				key = decryptor.decrypt(key) 
				print('Decrypted Key: ' + key)
				role = file_manager.get_role(key)
				if role:
					for permission in role['permissions']:
						if permission not in permissions:
							permissions.append(permission)
					
					self.pending_transmissions.append(	{
														'action' : constants.REQUEST_LOGIN,
														'code' : constants.HTTP_OK,
														'role' : role
														})
				else:
					self.pending_transmissions.append(	{
														'action' : constants.REQUEST_LOGIN,
														'code' : constants.HTTP_UNAUTHORIZED,
														'role' : 
															{
																'key' : key
															}
														})
		else: self.pending_transmissions.append({'action' : constants.REQUEST_LOGIN, 'code' : constants.HTTP_BAD_REQUEST})
		return permissions


	def build_file_change_inform(self, target):
		 self.pending_transmissions.append(	{
											'action' : constants.INFORM_FILE_CHANGE, 
											'target' : target,
											'hash' : file_manager.get_hash(target),
											'data' : file_manager.get_file(target)
											})
	