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

from client import ClientThread
from response_handle import ResponseHandler
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
			ClientThread(conn, addr[0]).start() # A new Thread gets startet that handles the conenction of this client
		except socket.timeout:
			pass
		except KeyboardInterrupt:
			break


	server.close()

main()
