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

# GENERAL VARIABLES
PORT = 52323
VERSION = '1.0.0'

# THREADING VARIABLES
connected_ips = []

class RequestHandler():
	pass

class ClientTread(threading.Thread):

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
		


def main():
	# Server Setup
	monitoring.saveVersion(VERSION)
	monitoring.saveExecutionInterval(60)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #The server is running over the Internet with the TCP protocoll
	server.bind(("", PORT)) #The server uses the computers own IP and the predefined PORT
	server.listen(200) #The server can handle up to 200 clients at once
	server.settimeout(60)

	while True:
		monitoring.timeExecution()
		try:
			conn, addr = server.accept() # The server tries to accept a connection. If nobody connects the timeout exeption is thrown.
			connected_ips.append(addr[0])
			ClientTread(conn, addr[0]).start() # A new Thread gets startet that handles the conenction of this client
		except socket.timeout:
			pass
		except KeyboardInterrupt:
			break


	server.close()

main()
