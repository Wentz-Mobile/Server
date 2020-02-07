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

REQUEST_SIGN_UP	= 1;

class ClientThread(threading.Thread):



	def __init__(self, conn, ip):
		super().__init__()
		self.conn = conn
		self.conn.settimeout(2)
		self.name = 'Client {}'.format(ip);
		self.ip = ip
		self.running = True
		self.handler = Handler()
		self.sign_up()
	
	# ------------------- #
	def sign_up(self):
		data = self.receive()
		if data:
			self.client_info, send = self.handler.handle_sign_up(data)
			self.send(send)
		else:
			self.disconnect()
					   			 
	def disconnect(self):
		print('client disconected')
		self.running = False
		self.conn.close()

	

	def run(self):
		while self.running:
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
			return data
			# HANDLE EXCEPTIONS
		except timeout:
			pass
		except KeyError:
			self.send({'code': HTTP_BAD_REQUEST, 'request': -1})
		except json.decoder.JSONDecodeError:
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
	def handle_sign_up(self, request):
		if has_keys(request, {'os', 'version', 'hash'}): # Validate the request
			client_info =	{
							'os' : request['os'] # Add everything necessary to the client information
							}
			return client_info, {'action' : REQUEST_SIGN_UP, 'code' : HTTP_OK} # Return the client info and what to respond to the client