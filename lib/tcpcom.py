# tcpcom.py
# AP

from threading import Thread
import thread
import socket
import time
import sys

TCPCOM_VERSION = "1.11 - Jan. 21, 2016"

# ================================== Server ================================
# ---------------------- class TCPServer ------------------------
class TCPServer(Thread):
    isVerbose = False
    PORT_IN_USE = "PORT_IN_USE"
    CONNECTED = "CONNECTED"
    LISTENING = "LISTENING"
    TERMINATED = "TERMINATED"
    MESSAGE = "MESSAGE"

    def __init__(self, port, stateChanged, isVerbose = False):
        Thread.__init__(self)
        self.port = port
        self.stateChanged = stateChanged
        TCPServer.isVerbose = isVerbose
        self.isClientConnected = False
        self.terminateServer = False
        self.isServerRunning = False
        self.start()

    def run(self):
        TCPServer.debug("TCPServer thread started")
        HOSTNAME = "" # Symbolic name meaning all available interfaces
        self.conn = None
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # close port when process exits
        TCPServer.debug("Socket created")
        try:
            self.serverSocket.bind((HOSTNAME, self.port))
        except socket.error as msg:
            print "Fatal error while creating TCPServer: Bind failed.", msg[0], msg[1]
            sys.exit()
        try:    
            self.serverSocket.listen(10)
        except:
            print "Fatal error while creating TCPServer: Port", self.port, "already in use"
            try:
                self.stateChanged(TCPServer.PORT_IN_USE, str(self.port))
            except Exception, e:
               print "Caught exception in TCPServer.PORT_IN_USE:", e
            sys.exit()

        try:
            self.stateChanged(TCPServer.LISTENING, str(self.port))
        except Exception, e:
            print "Caught exception in TCPServer.LISTENING:", e

        self.isServerRunning = True
                
        while True:
            # wait to accept a connection - blocking call
            TCPServer.debug("Calling blocking accept()...")
            self.conn, self.addr = self.serverSocket.accept()
            if self.terminateServer:
                break
            self.isClientConnected = True
            self.socketHandler = ServerHandler(self)
            self.socketHandler.setDaemon(True)  # necessary to terminate thread at program termination
            self.socketHandler.start()
            try: 
                self.stateChanged(TCPServer.CONNECTED, self.addr[0])
            except Exception, e:
                print "Caught exception in TCPServer.CONNECTED:", e
        self.conn.close()
        self.serverSocket.close()
        self.isClientConnected = False
        try:
            self.stateChanged(TCPServer.TERMINATED, "")
        except Exception, e:
            print "Caught exception in TCPServer.TERMINATED:", e
        TCPServer.debug("TCPServer thread terminated")

    def terminate(self):
        TCPServer.debug("Calling terminate()")
        if not self.isServerRunning:
            TCPServer.debug("Server not running")
            return
        self.terminateServer = True
        TCPServer.debug("Disconnect by a dummy connection...")
        if self.conn != None:
            self.conn.close()
            self.isClientConnected = False
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', self.port))  # dummy connection to get out of accept()
        
    def disconnect(self):
        if self.isClientConnected:
            self.isClientConnected = False
            try:
                self.stateChanged(TCPServer.LISTENING, str(self.port))
            except Exception, e:
                print "Caught exception in TCPServer.LISTENING:", e
            self.conn.close()

    def sendMessage(self, msg):
        TCPServer.debug("sendMessage() with msg: " + msg)
        if not self.isClientConnected:
            TCPServer.debug("Not connected")
            return
        try:
            self.conn.sendall(msg + "\0")    
        except:
            TCPClient.debug("Exception in sendMessage()")

    def isConnected(self):
        time.sleep(0.001)
        return self.isClientConnected
    
    def isTerminated(self):
        time.sleep(0.001)
        return self.terminateServer

    @staticmethod
    def debug(msg):
        if TCPServer.isVerbose:
            print "   TCPServer-> " + msg
 
    @staticmethod
    def getVersion():
          return TCPCOM_VERSION
   
# ---------------------- class ServerHandler ------------------------
class ServerHandler(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        TCPServer.debug("ServerHandler started")
        bufSize = 4096
        try:
            while True:
                data = ""
                reply = ""
                isRunning = True
                while not reply[-1:] == "\0":
                    TCPServer.debug("Calling blocking conn.recv()")
                    reply = self.server.conn.recv(bufSize)
                    if reply == None or len(reply) == 0: # Client disconnected
                        TCPServer.debug("conn.recv() returned None")
                        isRunning = False
                        break
                    data += reply
                if not isRunning:
                    break
                TCPServer.debug("Received msg: " + data + " len: " + str(len(data)))
                junk = data.split("\0")  # more than 1 message may be received if
                                         # transfer is fast. data: xxxx\0yyyyy\0zzz\0
                for i in range(len(junk) - 1):
                    try:
                        self.server.stateChanged(TCPServer.MESSAGE, junk[i])
                    except Exception, e:
                        print "Caught exception in TCPServer.MESSAGE:", e
        except:  # May happen if client peer is resetted
            TCPServer.debug("Exception from blocking conn.recv(), Msg: " + str(sys.exc_info()[0]) + \
              " at line # " +  str(sys.exc_info()[-1].tb_lineno))

        self.server.disconnect()
        TCPServer.debug("ServerHandler terminated")


# ================================== Client ================================
# -------------------------------- class TCPClient --------------------------
class TCPClient():
    isVerbose = False
    CONNECTING = "CONNECTING"
    CONNECTION_FAILED = "CONNECTION_FAILED"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    MESSAGE = "MESSAGE"

    def __init__(self, ipAddress, port, stateChanged, isVerbose = False):
        self.isClientConnected = False
        self.isClientConnecting = False
        self.ipAddress = ipAddress
        self.port = port
        self.stateChanged = stateChanged
        TCPClient.isVerbose = isVerbose
                  
    def sendMessage(self, msg, responseTime = 0):
        TCPClient.debug("sendMessage() with msg = " + msg)
        if not self.isClientConnected:
            TCPClient.debug("sendMessage(): Connection closed.")
            return None
        reply = None
        try:
            msg += "\0";  # Append \0
            rc = self.sock.sendall(msg)
            if responseTime > 0:
                reply = self._waitForReply(responseTime)  # Blocking
        except:
            TCPClient.debug("Exception in sendMessage()")
            self.disconnect()
    
        return reply
    
    def _waitForReply(self, responseTime):
        TCPClient.debug("Calling _waitForReply()")
        self.receiverResponse = None
        startTime = time.time()
        while self.isClientConnected and self.receiverResponse == None and time.time() - startTime < responseTime:
            time.sleep(0.01)
        if self.receiverResponse == None:    
            TCPClient.debug("Timeout while waiting for reply")
        else:    
            TCPClient.debug("Response = " + self.receiverResponse + " time elapsed: " + str(int(1000 * (time.time() - startTime))) + " ms")
        return self.receiverResponse
    
    def connect(self, timeout = None):
        try:
            self.stateChanged(TCPClient.CONNECTING, self.ipAddress)
        except Exception, e:
            print "Caught exception in TCPClient.CONNECTING:", e
        try:
            self.isClientConnecting = True
            host = (self.ipAddress, self.port)
            if self.ipAddress == "localhost" or self.ipAddress == "127.0.0.1":
                timeout = None  # do not use timeout for local host, to avoid error message "java.net..."
            self.sock = socket.create_connection(host, timeout)
            self.sock.settimeout(None)
            self.isClientConnecting = False
            self.isClientConnected = True
            try:
                self.stateChanged(TCPClient.CONNECTED, self.ipAddress)
            except Exception, e:
                print "Caught exception in TCPClient.CONNECTED:", e
        except:
            self.isClientConnecting = False
            try:
                self.stateChanged(TCPClient.CONNECTION_FAILED, self.ipAddress)
            except Exception, e:
                print "Caught exception in TCPClient.CONNECTION_FAILED:", e
            TCPClient.debug("Connection failed.")
            return False
        ClientHandler(self)
        return True
    
    def disconnect(self):
        TCPClient.debug("Client.disconnect()")
        if not self.isClientConnected:
            TCPClient.debug("Connection already closed")
            return
        self.isClientConnected = False
        TCPClient.debug("Closing socket")
        try: # catch Exception "transport endpoint is not connected"
            self.sock.shutdown(socket.SHUT_RDWR)  
        except:
            pass
        self.sock.close()
        try:
            self.stateChanged(TCPClient.DISCONNECTED, "")
        except Exception, e:
            print "Caught exception in TCPClient.DISCONNECTED:", e
    
    def isConnecting(self):
        time.sleep(0.001)
        return self.isClientConnecting

    def isConnected(self):
        time.sleep(0.001)
        return self.isClientConnected
    
    @staticmethod
    def debug(msg):
        if TCPClient.isVerbose:
            print "   TCPClient-> " + msg

    @staticmethod
    def getVersion():
          return TCPCOM_VERSION

# -------------------------------- class ClientHandler ---------------------------
class ClientHandler(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.start()
                
    def run(self):
        TCPClient.debug("ClientHandler thread started")
        while True:
            try:
                junk = self.readResponse().split("\0")
                # more than 1 message may be received 
                # if transfer is fast. data: xxxx\0yyyyy\0zzz\0
                for i in range(len(junk) - 1):
                    try:
                        self.client.stateChanged(TCPClient.MESSAGE, junk[i])
                    except Exception, e:
                        print "Caught exception in TCPClient.MESSAGE:", e
            except:    
                TCPClient.debug("Exception in readResponse() Msg: " + str(sys.exc_info()[0]) + \
                  " at line # " +  str(sys.exc_info()[-1].tb_lineno))
                self.client.disconnect()
                break
        TCPClient.debug("ClientHandler thread terminated")

    def readResponse(self):
        TCPClient.debug("Calling readResponse")
        bufSize = 4096
        data = ""
        while not data[-1:]  ==  "\0":
            try:
                reply = self.client.sock.recv(bufSize)  # blocking
            except:
                TCPClient.debug("Exception from blocking conn.recv(), Msg: " + str(sys.exc_info()[0]) + \
                  " at line # " +  str(sys.exc_info()[-1].tb_lineno))
                raise Exception("Exception from blocking sock.recv()")
            data += reply
        return data


