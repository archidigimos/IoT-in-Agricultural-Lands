import sqlite3 as lite
import sys
import time

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

from twisted.python import log
from twisted.internet import reactor

connectionsTCP={}
factory = WebSocketServerFactory(u"ws://172.24.1.1:9000")
factory1 = WebSocketClientFactory(u"ws://ec2-35-163-167-156.us-west-2.compute.amazonaws.com:80")


connectionsTCP={}
con = lite.connect('database.db')
cur = con.cursor()

#---------------------------------------------------------------------------------
class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            data_parsed_s = payload.split("-")

            if data_parsed_s[0]=="LOGIN":
                connectionsTCP[data_parsed_s[1]]=self
            if data_parsed_s[0]=="DATA":
                epoch_time = int(time.time())
                if "global server" in connectionsTCP:
                    connectionsTCP["global server"].sendMessage(payload+"-"+str(epoch_time))
                if data_parsed_s[1]=="SENSOR1":
                    cur.execute("INSERT INTO SENSOR_ONE VALUES (?, ?, ?, ?, ?);",(epoch_time,int(data_parsed_s[2]),int(data_parsed_s[3]),int(data_parsed_s[4]),int(data_parsed_s[5])))
                if data_parsed_s[1]=="SENSOR2":
                    cur.execute("INSERT INTO SENSOR_TWO VALUES (?, ?, ?);",(epoch_time,int(data_parsed_s[2]),int(data_parsed_s[3])))
                if data_parsed_s[1]=="SENSOR3":
                    cur.execute("INSERT INTO SENSOR_THREE VALUES (?, ?, ?, ?);",(epoch_time,int(data_parsed_s[2]),int(data_parsed_s[3]),int(data_parsed_s[4])))
                if data_parsed_s[1]=="SENSOR4":
                    cur.execute("INSERT INTO SENSOR_FOUR VALUES (?, ?, ?);",(epoch_time,int(data_parsed_s[2]),int(data_parsed_s[3])))
                con.commit()

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

#------------------------------------------------------------------------------------
class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
        connectionsTCP["global server"]=self
        self.sendMessage("LOGIN-RPI3_1")

    def onOpen(self):
        connectionsTCP["global server"]=self
        def ping():
            self.sendMessage("rpi3_1..ping")
            self.factory.reactor.callLater(1, ping)

        # start sending messages every second ..
        ping()
        
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
	    self.sendMessage("DATA-RPI3_1_talking-data_received-reply")
            data_parsed = payload.split("-")
            if data_parsed[0] in connectionsTCP:
                connectionsTCP[data_parsed[0]].sendMessage(data_parsed[1])

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory.protocol = MyServerProtocol
    factory1.protocol = MyClientProtocol

    reactor.connectTCP("ec2-35-163-167-156.us-west-2.compute.amazonaws.com", 80, factory1)
    reactor.listenTCP(9000, factory)

    reactor.run()

con.close()
