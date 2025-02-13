#SIM800Modem.py

import RPi.GPIO as GPIO
import time

VERBOSE = False
P_POWER = 11 # Power pin
P_RESET = 12 # Reset pin

def debug(text):
    if VERBOSE:
        print("Debug:---", text)

def resetModem():
    debug("Resetting modem...")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_RESET, GPIO.OUT)
    GPIO.output(P_RESET, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(P_RESET, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(P_RESET, GPIO.LOW)
    time.sleep(3)

def togglePower():
    debug("Toggling power...")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_POWER, GPIO.OUT)
    GPIO.output(P_POWER, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(P_POWER, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(P_POWER, GPIO.LOW)

def isReady(ser):
    # Resetting to defaults
    cmd = 'ATZ\r'
    debug("Cmd: " + cmd)
    ser.write(cmd)
    time.sleep(2)
    reply = ser.read(ser.inWaiting())
    time.sleep(8) # Wait until connected to net
    debug("Reply: " + reply)
    return ("OK" in reply)
   
def connectGSM(ser, apn):
    # Login to APN, no userid/password needed
    cmd = 'AT+CSTT="' + apn + '"\r'
    debug("Cmd: " + cmd)
    ser.write(cmd)
    time.sleep(3)
    
    # Bringing up network
    cmd = "AT+CIICR\r"
    debug("Cmd: " + cmd)
    ser.write(cmd)
    time.sleep(5)
    
    # Getting IP address
    cmd = "AT+CIFSR\r"
    debug("Cmd: " + cmd)
    ser.write(cmd)
    time.sleep(3)
    
    # Returning all messages from modem
    reply = ser.read(ser.inWaiting())
    debug("connectGSM() retured:\n" + reply)
    return reply

def connectTCP(ser, host, port):
    cmd = 'AT+CIPSTART="TCP","' + host + '","' + str(port) + '"\r'
    ser.write(cmd)
    time.sleep(5)
    reply = ser.read(ser.inWaiting())
    debug("connctTCP() retured:\n" + reply)
    return reply

def sendHTTPRequest(ser, host, request):
    ser.write("AT+CIPSEND\r")
    time.sleep(2)
    request = "GET " + request + " HTTP/1.1\r\nHost: " + host + "\r\n\r\n" 
    ser.write(request + chr(26))  # data<^Z>
    time.sleep(2)
    
def closeTCP(ser, showResponse = False):
    ser.write("AT+CIPCLOSE=1\r") 
    reply = ser.read(ser.inWaiting())
    debug("closeTCP() retured:\n" + reply)
    if showResponse:
        print("Server reponse:\n" + reply[(reply.index("SEND OK") + 9):])
    time.sleep(2)
    
def getIPStatus(ser):
    cmd = "AT+CIPSTATUS\n"
    ser.write(cmd)
    time.sleep(1)
    reply = ser.read(ser.inWaiting())
    return reply
