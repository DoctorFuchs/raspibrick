# WebServer1.py

import socket 
import time
import math

host = "www.xxx.dx.am"
port = 80

for x in range(0, 101, 5):
    y = 0.5 + 0.5 * math.sin(0.1 * x) 
    print x, y
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((host , port))
    request = "GET /insert.php?x=" + str(x) + "&y=" + str(y) + \
              " HTTP/1.1\r\nHost: " + host + "\r\n\r\n" 
    s.send(request)
    s.shutdown(1)
    s.close()
    time.sleep(5)
print "Done"

