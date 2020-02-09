import threading
import json
from socket import timeout

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

REQUEST_SIGN_UP	= 1

TARGET_FILE_DATES
TARGET_FILE_CREATORS

class ClientThread(threading.Thread):

	def __init__(self, conn, ip):
		super().__init__()
		self.conn = conn
		self.name = 'Client {}'.format(ip);
		self.ip = ip
		self.running = True
		self.handler = Handler()
		self.sign_up()
	
	# ------------------- #
	def sign_up(self):
		self.conn.settimeout(1)
		data = self.receive()
		if data:
			self.os, was_sign_up_valide = self.handler.handle_sign_up(data)
			if not was_sign_up_valide:
				self.disconnect()
		else:
			self.disconnect()

		self.conn.settimeout(2)
					   			 
	def disconnect(self):
		self.running = False
		self.conn.close()

	

	def run(self):
		while self.running:
			for transmission in self.handler.pending_transmissions:
				self.send(transmission)

			self.receive()

	def send(self, jdic):
		self.conn.send(json.dumps(jdic).encode('utf8'))

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
		except Exception as e:
			self.send({'code': HTTP_BAD_REQUEST, 'request': -1})
			self.disconnect()
		except ConnectionResetError:
			self.disconnect()
		except ConnectionAbortedError:
			self.disconnect()
		return None
		
		
def has_keys(dict, keys):
	if isinstance(keys, str):
		return keys in dict

	for key in keys:
		if not key in dict:
			return False
	return True

class Handler(object):

	def __init__():
		self.pending_transmissions = []

	def handle_sign_up(self, request):
		if has_keys(request, {'action','os', 'version', 'hash'}) and request['action'] is REQUEST_SIGN_UP: # Validate the request
			os = request['os']
			self.pending_transmissions.append({'action' : REQUEST_SIGN_UP, 'code' : HTTP_OK})

			hashes = request['hash']


			return os, True # Return the client info

		self.pending_transmissions.append({'action' : REQUEST_SIGN_UP, 'code' : HTTP_BAD_REQUEST})
		return None, False