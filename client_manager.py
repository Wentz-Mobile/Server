from client import ClientThread

clients = [] # List with all connected clients

def refresh():
    for client in clients:
        if not client.running:
            clients.remove(client)

def addClient(conn, ip):
    client = ClientThread(conn, ip) # A new client gets created
    client.start() # The new client gets started
    clients.append(client) # The new client gets saved
