# rfcomm-server.py

from bluetooth import *
import StringIO
import os
import pwd
import grp

VERSION = "V1.02"

def saveData(data, filename):
    '''
    Writes the given string data into a binary file.
    @param data: the data to store (as string type)
    @param filename: a valid filename in the local file space
    '''
    file = open(filename, "wb")
    file.write(data)
    file.close()
    uid = pwd.getpwnam("pi").pw_uid
    gid = grp.getgrnam("pi").gr_gid
    os.chown(filename, uid, gid)


server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "RaspiServer",
                  service_id = uuid,
                  service_classes = [uuid, SERIAL_PORT_CLASS],
                  profiles = [SERIAL_PORT_PROFILE],
#                   protocols = [OBEX_UUID]
                    )
print "RFComm Server", VERSION, "started"
isRunning = True
while isRunning:
    try:
        print "Waiting for connection on RFCOMM channel %d" % port
        client_sock, client_info = server_sock.accept()
        print "Accepted connection from ", client_info

        data = StringIO.StringIO()
        try:
            while True:
                block = client_sock.recv(1024)
                data.write(block)
        except IOError:
            pass
        print "disconnected"
        client_sock.close()
        print "Received data with size: ", len(data.getvalue()), "bytes"
        saveData(data.getvalue(), "/home/pi/scripts/MyApp.py")
        print "Saved in /home/pi/scripts/MyApp.py"
        data.close()
    except Exception, e:
        print "Exception", e
        isRunning = False
server_sock.close()
print "Server terminated"
