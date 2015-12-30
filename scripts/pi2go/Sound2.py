# Sound2.py

from raspibrick import *

morse = {
'a':'.-'   , 'b':'-...' , 'c':'-.-.' , 'd':'-..'  , 'e':'.'    ,
'f':'..-.' , 'g':'--.'  , 'h':'....' , 'i':'..'   , 'j':'.---' ,
'k':'-.-'  , 'l':'.-..' , 'm':'--'   , 'n':'-.'   , 'o':'---'  ,
'p':'.--.' , 'q':'--.-' , 'r':'.-.'  , 's':'...'  , 't':'-'    ,
'u':'..-'  , 'v':'...-' , 'w':'.--'  , 'x':'-..-' , 'y':'-.--' ,
'z':'--..' , '1':'.----', '2':'..---', '3':'...--', '4':'....-',
'5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.',
'0':'-----'}


def emitDot():
    robot.playTone(1000, unit)

def emitDash():
    robot.playTone(1000, 3 * unit)

def transmit(text):
    for c in text:
        print(c)
        if c == " ":
            Tools.delay(7 * unit)
        else:
            c = c.lower()
            if c in morse:
                k = morse[c]
                for x in k:
                    if x == '.':
                        emitDot()
                    else:
                        emitDash()
                    Tools.delay(unit)
            Tools.delay(3 * unit)

robot = Robot()
unit = 100
text = "cq cq cq de hb9abh pse k"
transmit(text)

print "All done"
