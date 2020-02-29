import os
import threading
import time
import colorama
from colorama import Fore, Back, Style
colorama.init()

startTime = time.time()

version = '1.0.1'
connectionCounter = 0

activeConnections = 0
connectionIP = []

executionInterval = 0
ellTime = 0

runntimeS = 60*60*24*300
runntimeD = 0
runntimeH = 0
runntimeM = 0

def show():
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("┌─{backWhite}SNIPP  {version}{reset}──────────────────────┬──────────────────────────────────┐".format(backWhite = Back.WHITE + Fore.BLACK, reset = Style.RESET_ALL, version = version.rjust(6)))
    print("│ ╔═╗                                │ RUNTIME             {day:3d}d {hour:2d}h {minute:2d}m │".format(day = runntimeD, hour = runntimeH, minute = runntimeM))
    print("│ ║{bar}║ {ip0} │ {ip5}  │ CONNECTION COUNTER  {connectionCounter:4d}         │".format(bar = getBar(5), ip0 = (connectionIP[0] if activeConnections > 0 else "").ljust(13), ip5 = (connectionIP[5] if activeConnections > 5 else "").ljust(13), connectionCounter = connectionCounter))
    print("│ ║{bar}║ {ip1} │ {ip6}  │                                  │".format(bar = getBar(4), ip1 = (connectionIP[1] if activeConnections > 1 else "").ljust(13), ip6 = (connectionIP[6] if activeConnections > 6 else "").ljust(13)))
    print("│ ║{bar}║ {ip2} │ {ip7}  │                                  │".format(bar = getBar(3), ip2 = (connectionIP[2] if activeConnections > 2 else "").ljust(13), ip7 = (connectionIP[7] if activeConnections > 7 else "").ljust(13)))
    print("│ ║{bar}║ {ip3} │ {ip8}  │                                  │".format(bar = getBar(2), ip3 = (connectionIP[3] if activeConnections > 3 else "").ljust(13), ip8 = (connectionIP[8] if activeConnections > 8 else "").ljust(13)))
    print("│ ║{bar}║ {ip4} │ {ip9}  │                                  │".format(bar = getBar(1), ip4 = (connectionIP[4] if activeConnections > 4 else "").ljust(13), ip9 = (connectionIP[7] if activeConnections > 9 else "").ljust(13)))
    print("│ ╚═╝                                │                                  │\n└────────────────────────────────────┴──────────────────────────────────┘")
    '''
    pass

   
def getBar(height):
    if height * 2 < activeConnections:
        return "█"
    elif height * 2 - 1 <= activeConnections:
        return "█" if activeConnections % (height * 2) == 0 else "▄"
    return " "

def saveVersion(nVersion):
    global version
    version = nVersion
    show()

def addConnection(ip):
    global connectionCounter, activeConnections
    connectionIP.append(ip)
    connectionCounter += 1
    activeConnections += 1
    show()

def removeConnection(ip):
    global activeConnections
    connectionIP.remove(ip)
    activeConnections -= 1
    show()

def saveTime():
    global runntimeM, runntimeH, runntimeD, runntimeS
    runntimeS = int(time.time() - startTime + 0.5)
    runntimeM = int((runntimeS/60.0)%60)
    runntimeH = int(runntimeS/60/60)
    runntimeD = int(runntimeH/24)
    runntimeH = int(runntimeH%24)

def saveExecutionInterval(time):
    global executionInterval
    executionInterval = time

def timeExecution():
    global ellTime
    if time.time() - ellTime >= executionInterval:
        ellTime = time.time()
        saveTime()
        show()
