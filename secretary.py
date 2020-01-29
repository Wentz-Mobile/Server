from datetime import date 
import time

REQUEST_ERROR             = -1
REQUEST_VALIDATE_PASSWORD = 1
REQUEST_EXTEND            = 2
REQUEST_LEAVE             = 3
REQUEST_REFRESH_CLOSET    = 10
REQUEST_EDIT_CLOSET       = 11
REQUEST_UPDATE_CLOSET     = 12

HTTP_OK 				 = 200
HTTP_NO_CONTENT          = 204
HTTP_BAD_REQUEST 		 = 400
HTTP_FORBIDDEN 			 = 403
HTTP_NOT_FOUND 			 = 404
HTTP_NOT_ACCEPTABLE 	 = 406
HTTP_REQUEST_TIMEOUT     = 408
HTTP_PRECONDITION_FAILED = 412
HTTP_LOCKED 			 = 423
HTTP_NOT_IMPLEMENTED 	 = 501

class LogEntry:

    input = None
    output = None
    ip = None

    request = None
    response = None

    def saveIP(self, ip):
        self.ip = ip

    def saveInput(self, input):
        self.input = input
    
    def saveOutput(self, output):
        self.output = output

    def writeLog(self):
        try:
            self.request = self.input['request']
        except:
            self.request = REQUEST_ERROR
        self.response = self.output['code']
        print(self.input['request'])
        if self.response == HTTP_BAD_REQUEST or self.response == HTTP_NOT_IMPLEMENTED:
            self.logError()

        if self.request == REQUEST_UPDATE_CLOSET:
            self.logReport()

        self.logConnection()

    def logConnection(self):
        log = getTimeStamp()
        log += '   '

        global conIdent
        log += getIdent(conIdent)
        conIdent += 1

        log += '   '
        log += getIP(self.ip)

        log += '   '
        log += getRequest(self.request)

        log += '   '
        log += getResponse(self.response)

        global conFile
        conFile.write(log + '\n')
        conFile.flush()

    def logError(self):

        log = getTimeStamp()
        log += '   '

        global errIdent
        log += getIdent(errIdent)
        errIdent += 1

        log += '   '
        log += getIP(self.ip)

        log += '...REQUEST: '
        log += str(self.input)
        log += '\n                                                       RESPONSE: '
        log += str(self.output)

        global errFile
        errFile.write(log + '\n')
        errFile.flush()

    def logReport(self):
        
        log = getTimeStamp()
        log += '   '

        global repIdent
        log += getIdent(repIdent)
        repIdent += 1

        log += '   '
        log += getReport(self.request)

        global repFile
        repFile.write(log + '\n')
        repFile.flush()

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

def getRequest(request):
    if   request == REQUEST_ERROR             : return 'REQUEST_ERROR.................'
    elif request == REQUEST_VALIDATE_PASSWORD : return 'REQUEST_VALIDATE_PASSWORD.....'
    elif request == REQUEST_EXTEND            : return 'REQUEST_EXTEND................'
    elif request == REQUEST_LEAVE             : return 'REQUEST_LEAVE.................'
    elif request == REQUEST_REFRESH_CLOSET    : return 'REQUEST_REFRESH_CLOSET........'
    elif request == REQUEST_EDIT_CLOSET       : return 'REQUEST_EDIT_CLOSET...........'
    elif request == REQUEST_UPDATE_CLOSET     : return 'REQUEST_UPDATE_CLOSET.........'

def getResponse(response):
    if   response == HTTP_OK                  : return 'OK..................'
    elif response == HTTP_NO_CONTENT          : return 'NO_CONTENT..........'
    elif response == HTTP_BAD_REQUEST         : return 'BAD_REQUEST............ERROR_IDENT: ' + getIdent(errIdent - 1)
    elif response == HTTP_FORBIDDEN           : return 'FORBIDDEN...........'
    elif response == HTTP_NOT_FOUND           : return 'NOT_FOUND...........'
    elif response == HTTP_NOT_ACCEPTABLE      : return 'NOT_ACCEPTABLE......'
    elif response == HTTP_REQUEST_TIMEOUT     : return 'REQUEST_TIMEOUT.....'
    elif response == HTTP_PRECONDITION_FAILED : return 'PRECONDITION_FAILED.'
    elif response == HTTP_LOCKED              : return 'LOCKED..............'
    elif response == HTTP_NOT_IMPLEMENTED     : return 'NOT_IMPLEMENTED........ERROR_IDENT: ' + getIdent(errIdent - 1)
    else                                      : return 'ERROR...............'

def getReport(request):
    if request == REQUEST_UPDATE_CLOSET : return 'CLOSET_UPDATED'

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

conFile = open('Protocoll\\connectionLog.txt','a')
errFile = open('Protocoll\\errorLog.txt','a')
repFile = open('Protocoll\\reportLog.txt','a')

conFile.write(getStartMessage())
conFile.write('TIME                            IDENT  IP              REQUEST                          RESPONSE\n')
errFile.write(getStartMessage())
errFile.write('TIME                            IDENT  IP              REQUEST/RESPONSE\n')
repFile.write(getStartMessage())
repFile.write('TIME                            IDENT  REPORT\n')

conFile.flush()
errFile.flush()
repFile.flush()

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

conFile.close()
errFile.close()
repFile.close()
