from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
        self.sendMessage("LOGIN-SENSOR2")

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            self.sendMessage("DATA-SENSOR2"+"-"+str(random_with_N_digits(5))+"-"+str(random_with_N_digits(5)))
            #self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.reactor.callLater(10, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://172.24.1.1:9000")
    factory.protocol = MyClientProtocol

    reactor.connectTCP("172.24.1.1", 9000, factory)
    reactor.run()