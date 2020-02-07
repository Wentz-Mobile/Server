#region IMPORTS
import hashlib
import json
import os
import random
import socket
import string
import threading
import time
import monitoring
import secretary
import file_manager
import client_manager
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

def main():
	# Server Setup
	monitoring.saveVersion(VERSION)
	monitoring.saveExecutionInterval(60)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #The server is running over the Internet with the TCP protocoll
	server.bind(("", PORT)) #The server uses the computers own IP and the predefined PORT
	server.listen(200) #The server can handle up to 200 clients at once
	server.settimeout(2)

	while True:
		try:
			client_manager.refresh()
			conn, addr = server.accept() # The server tries to accept a connection. If nobody connects the timeout exeption is thrown.
			client_manager.addClient(conn, addr[0]) # A new client gets added
		except socket.timeout:
			pass
		except KeyboardInterrupt:
			break


	server.close()

main()
