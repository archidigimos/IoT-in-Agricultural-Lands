import sqlite3 as lite
import sys
import time

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

webClients={}
sensor1 = lite.connect('/home/ebiw/cloud_files/databaserpi1.db')
sensor1_ = sensor1.cursor()
sensor2 = lite.connect('/home/ebiw/cloud_files/databaserpi2.db')
sensor2_ = sensor2.cursor()


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            #print("Text message received: {0}".format(payload.decode('utf8')))
            data_parsed = payload.split("-")
            epoch_time = int(time.time())

            if data_parsed[0]=="LOGIN":
                webClients[data_parsed[1]]=self
            if data_parsed[0]=="ADMIN":
                webClients["ADMIN"]=self
            if data_parsed[0]=="DATA":
                
                for client_conn in webClients.iterkeys():
                    if webClients[client_conn] == self:
                        break
                    else:
                        client_conn="NULL"
                if client_conn=="RPI3_1":
                    if "ADMIN" in webClients:
                        webClients["ADMIN"].sendMessage("DATA-"+data_parsed[1]+"-"+data_parsed[2]+"-"+data_parsed[3]+"-"+data_parsed[4]+"-"+data_parsed[5]+"-"+client_conn)
                    #if data_parsed[1]=="SENSOR1":
                        #sensor1_.execute("INSERT INTO SENSOR_ONE VALUES (?, ?, ?, ?, ?);",(epoch_time,int(data_parsed[2]),int(data_parsed[3]),int(data_parsed[4]),int(data_parsed[5])))
                    if data_parsed[1]=="SENSOR2":
                        sensor1_.execute("INSERT INTO SENSOR_TWO VALUES (?, ?, ?);",(epoch_time,int(data_parsed[2]),int(data_parsed[3])))
                    if data_parsed[1]=="SENSOR3":
                        sensor1_.execute("INSERT INTO SENSOR_THREE VALUES (?, ?, ?, ?);",(epoch_time,int(data_parsed[2]),int(data_parsed[3]),int(data_parsed[4])))
                    if data_parsed[1]=="SENSOR4":
                        sensor1_.execute("INSERT INTO SENSOR_FOUR VALUES (?, ?, ?);",(epoch_time,int(data_parsed[2]),int(data_parsed[3])))
                    sensor1.commit()
                    
                if client_conn=="RPI3_2":
                    if "ADMIN" in webClients:
                        webClients["ADMIN"].sendMessage(data_parsed[1]+"-"+data_parsed[2]+"-"+data_parsed[3]+"-"+client_conn)
                    if data_parsed[1]=="SENSOR1":
                        sensor2_.execute("INSERT INTO SENSOR_ONE VALUES (?, ?);",(epoch_time,int(data_parsed[2])))
                    if data_parsed[1]=="SENSOR2":
                        sensor2_.execute("INSERT INTO SENSOR_TWO VALUES (?, ?);",(epoch_time,int(data_parsed[2])))
                    if data_parsed[1]=="SENSOR3":
                        sensor2_.execute("INSERT INTO SENSOR_THREE VALUES (?, ?);",(epoch_time,int(data_parsed[2])))
                    if data_parsed[1]=="SENSOR4":
                        sensor2_.execute("INSERT INTO SENSOR_FOUR VALUES (?, ?);",(epoch_time,int(data_parsed[2])))
                    if data_parsed[1]=="SENSOR5":
                        sensor2_.execute("INSERT INTO SENSOR_FIVE VALUES (?, ?);",(epoch_time,int(data_parsed[2])))
                    sensor2.commit()

            if data_parsed[0]=="USERDATA":
                if data_parsed[1] in webClients:
                    webClients[data_parsed[1]].sendMessage(data_parsed[2]+"-"+data_parsed[3])

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://sp.ebiw.com:9000")
    factory.protocol = MyServerProtocol

    reactor.listenTCP(9000, factory)
    reactor.run()

sensor1.close()
sensor2.close()
