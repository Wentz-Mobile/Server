import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.178.81", 52323))

sock.send(json.dumps({}))