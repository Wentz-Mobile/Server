from datetime import date 
import time

HTTP_NOT_IMPLEMENTED 	 = 501

class LogEntry:

    def saveIP(self, ip):
        self.ip = ip

    def writeLog(self):
        pass

    def logConnection(self):
        pass

    def logError(self):
        pass

    def logReport(self):
        pass

def getIdent(ident):
    output = ''
    for i in range(4 - len(str(ident))):
        output += '0'
    output += str(ident)
    return output

def getIP(ip):
    subStr = ip[10:]
    while len(subStr) < 3:
        subStr += '.'
    return ip[:10] + subStr

def getTimeStamp():
    timedateStamp = '[d: '
    timedateStamp += date.today().strftime('%d-%m-%Y')
    timedateStamp += '   t: '
    timedateStamp += time.strftime("%H.%M.%S", time.localtime())
    timedateStamp += ']'
    return timedateStamp

def getStartMessage():
    startMessage = getTimeStamp()
    startMessage += '   --------Server is online--------\n'
    return startMessage

conFile = None
errFile = None
repFile = None

conIdent, errIdent, repIdent = 0, 0, 0
#region Debug
#request = [-1, 1, 2, 3, 10, 11, 12]
#response = [200, 204, 400, 403, 404, 406, 408, 412, 423, 501]
#
#log = Log()
#log.saveIP('192.123.0.9')
#
#for req in range(len(request)):
#   for res in range(len(response)):
#        log.saveInput({'request':request[req]})
#        log.saveOutput({'code':response[res]})
#        log.writeLog()
#endregion
