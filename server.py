#region IMPORTS
import constants
import hashlib
import json
import os
import random
import socket
import threading
import time
import secretary
import file_manager
import client_manager
#endregion


# GENERAL VARIABLES
PORT = 52323
VERSION = '1.0.0'

file_manager.get_file(constants.TARGET_FILE_CREATORS)

def main():
	# Server Setup
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
