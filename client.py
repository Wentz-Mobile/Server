import threading
import json
import file_manager
import encryptor
from socket import timeout

HTTP_OK 				 = 200
HTTP_NO_CONTENT          = 204
HTTP_BAD_REQUEST 		 = 400
HTTP_UNAUTHORIZED 		 = 401
HTTP_FORBIDDEN 			 = 403
HTTP_NOT_FOUND 			 = 404
HTTP_NOT_ACCEPTABLE 	 = 406
HTTP_PRECONDITION_FAILED = 412
HTTP_EXPECTATION_FAILED  = 417
HTTP_LOCKED 			 = 423
HTTP_NOT_IMPLEMENTED 	 = 501

REQUEST_SIGN_UP	= 1
REQUEST_LOGIN	= 2

INFORM_FILE_CHANGE = 200

TARGET_FILE_CREATORS	= 2
TARGET_FILE_DATES		= 3

class ClientThread(threading.Thread):

	def __init__(self, conn, ip):
		super().__init__()
		self.conn = conn
		self.name = 'Client {}'.format(ip)
		self.ip = ip
		self.running = True
		self.handler = Handler()
		self.decryptor = encryptor.Decryptor()
		self.sign_up()
	
	# ------------------- #
	def sign_up(self):
		self.conn.settimeout(1)
		data = self.receive()
		if data:
			self.os, self.encryptor, is_valide = self.handler.handle_sign_up(data)
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
				if data['action'] is REQUEST_LOGIN:
					self.handler.handle_login(data)

	def send(self, jdic):
		self.conn.send((json.dumps(jdic) + '\n').encode('utf8'))

	def receive(self):
		try:
			data = self.conn.recv(1024) # Receive 1024 byte (or try at least)
		
			if data == b'': # HANDLE 0 BYTES (Client disconnected)
				self.disconnect()
				return None
			data = json.loads(data)
			print(data)
			return data
		# HANDLE EXCEPTIONS
		except timeout:
			pass
		except KeyError:
			self.send({'code': HTTP_BAD_REQUEST, 'request': -1})
		except json.decoder.JSONDecodeError:
			print('decode error')
			self.send({'code': HTTP_BAD_REQUEST, 'request': -1})
		except ConnectionResetError:
			self.disconnect()
		except ConnectionAbortedError:
			self.disconnect()
		except Exception:
			self.send({'code': HTTP_BAD_REQUEST, 'request': -1})
			self.disconnect()
		
		return None
		
		
def has_keys(dict, keys):
	for key in keys:
		if not key in dict:
			return False
	return True

class Handler(object):

	def __init__(self):
		self.pending_transmissions = []

	def handle_sign_up(self, request):
		if has_keys(request, ['action','os', 'version', 'N', 'hash']) and request['action'] is REQUEST_SIGN_UP: # Validate the request
			os = request['os']
			encryptor = encryptor.Encryptor(request['N'])
			hashes = request['hash']
			if 'creators' not in hashes or file_manager.has_changed(hashes['creators'], TARGET_FILE_CREATORS):
				self.build_file_change_inform(TARGET_FILE_CREATORS)

			if 'date' not in hashes or file_manager.has_changed(hashes['dates'], TARGET_FILE_DATES):
				self.build_file_change_inform(TARGET_FILE_DATES)

			self.pending_transmissions.append({'action' : REQUEST_SIGN_UP, 'code' : HTTP_OK})
			return os, True # Return the client info

		self.pending_transmissions.append({'action' : REQUEST_SIGN_UP, 'code' : HTTP_BAD_REQUEST})
		return None, encryptor,False

	def handle_login(self, request):
			if 'keys' in request:
				for key in request['keys']:
					role = file_manager.get_role(key)
					if role:
						self.pending_transmissions.append(	{
															'action' : REQUEST_LOGIN,
															'code' : HTTP_OK,
															'role' : role
															})
					else:
						self.pending_transmissions.append(	{
															'action' : REQUEST_LOGIN,
															'code' : HTTP_UNAUTHORIZED,
															'role' : 
																{
																	'key' : key
																}
															}
			self.pending_transmissions.append({'action' : REQUEST_SIGN_UP, 'code' : HTTP_BAD_REQUEST})


	def build_file_change_inform(self, target):
		 self.pending_transmissions.append(	{
											'action' : INFORM_FILE_CHANGE, 
											'target' : target,
											'hash' : file_manager.get_hash(target),
											'data' : file_manager.get_file(target)
											})
	