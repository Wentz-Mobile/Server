import threading

class ClientThread(threading.Thread):

	def __init__(self, conn, ip):
		super().__init__()
		self.conn = conn
		self.conn.settimeout(2)
		self.name = ip
		self.ip = ip
		self.log = secretary.LogEntry()
		self.running = True
		monitoring.addConnection(ip)
		self.log.saveIP(ip)
		self.client_info = self.request_sign_up()
	
	# ------------------- #
	def resources_available(self, target):
		return True

	def disconnect(self):
		self.running = False
		monitoring.removeConnection(self.name)
		connected_ips.remove(self.ip)
		self.conn.close()

	def send(self, jdic):
		self.log.writeLog()
		self.conn.send(json.dumps(jdic).encode('utf8'))

	def run(self):
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
				if data['action'] == REQUEST_SIGN_UP:
					pass
			
			# HANDLE EXCEPTIONS
			except ConnectionResetError:
				self.disconnect()
			except ConnectionAbortedError:
				self.disconnect()

			except KeyError:
				self.send({'code': HTTP_BAD_REQUEST, 'request': -1})
			except json.decoder.JSONDecodeError:
				self.send({'code': HTTP_BAD_REQUEST, 'request': -1})
			except Exception as e:
				self.send({'code': HTTP_BAD_REQUEST, 'request': -1})
				self.disconnect()

		self.disconnect()




