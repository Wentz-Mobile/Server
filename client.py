import threading
import json
from socket import timeout
from response_handle import ResponseHandler

class ClientThread(threading.Thread):



	def __init__(self, conn, ip):
		super().__init__()
		self.conn = conn
		self.conn.settimeout(2)
		self.name = 'Client {}'.format(ip);
		self.ip = ip
		self.running = True
		self.sign_up()
	
	# ------------------- #
	def sign_up(self):
		data = receive()
		if data:
			if has_keys(data, ['os', 'version', 'hash']):




	def disconnect(self):
		self.running = False
		self.conn.close()

	

	def run(self):
		while self.running:
			receive()

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

class handler(object):
    pass




