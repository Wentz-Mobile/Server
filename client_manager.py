from client import ClientThread
import monitoring

clients = [] # List with all connected clients
monitoring.saveVersion('v1.0.0')
monitoring.saveExecutionInterval(60)

def refresh():
    for client in clients:
        if not client.running:
            monitoring.removeConnection(client.ip)
            clients.remove(client)
    monitoring.timeExecution()

def addClient(conn, ip):
    client = ClientThread(conn, ip) # A new client gets created
    client.start() # The new client gets started
    clients.append(client) # The new client gets saved
    monitoring.addConnection(client.ip)
