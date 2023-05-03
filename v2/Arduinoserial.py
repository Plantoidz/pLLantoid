import serial
import time
import os
import random
import regex_spm

startMarker = '<'
endMarker = '>'
dataStarted = False
dataBuf = ""
messageComplete = False

#========================
#========================
    # the functions

def setupSerial(baudRate, serialPortName):
    
    global  serialPort
    
    serialPort = serial.Serial(port= serialPortName, baudrate = baudRate)

    print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))

    waitForArduino()

#========================

def sendToArduino(stringToSend):
    
        # this adds the start- and end-markers before sending
    global startMarker, endMarker, serialPort
    
    stringWithMarkers = (startMarker)
    stringWithMarkers += stringToSend
    stringWithMarkers += (endMarker)

    serialPort.write(stringWithMarkers.encode('utf-8')) # encode needed for Python3
    

#==================

def recvLikeArduino():

    global startMarker, endMarker, serialPort, dataStarted, dataBuf, messageComplete

    if serialPort.inWaiting() > 0 and messageComplete == False:
        x = serialPort.read().decode("utf-8") # decode needed for Python3
        
        if dataStarted == True:
            if x != endMarker:
                dataBuf = dataBuf + x
            else:
                dataStarted = False
                messageComplete = True
        elif x == startMarker:
            dataBuf = ''
            dataStarted = True
    
    if (messageComplete == True):
        messageComplete = False
        return dataBuf
    else:
        return "XXX"

#==================

def waitForArduino():

    # wait until the Arduino sends 'Arduino is ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded
    
    print("Waiting for Arduino to reset")
     
    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == 'XXX'): 
            print(msg)



#====================
#====================
    # the program



waves = [9] * 10;

setupSerial(9600, "/dev/cu.usbserial-AK08LLRZ")
count = 0
prevTime = time.time()

sendToArduino("awake");


file = open("datapoints.txt", "w")

while True:

    # check for a reply
     arduinoReply = recvLikeArduino()
     if not (arduinoReply == 'XXX'):

      #  print(arduinoReply)

        match regex_spm.fullmatch_in(arduinoReply):
            case r"Waving: (\d)" as m:

                        print ("Waved at " + m[1]);

                        if(not waves[int(m[1])]):

                            sendToArduino("asleep")
                            sendToArduino("fire")

                            path = "/Users/ya/LLMs/PLLantoid/haikus/mp3s/"
                            dir_list = os.listdir(path)
                            fh = random.choice(dir_list);
                            os.system("mpg123 ~/LLMs/PLLantoid/haikus/mp3s/" + fh)

                            sendToArduino("fire")
                            sendToArduino("awake")

                            waves[int(m[1])] = 1;

                        else:

                            waves[int(m[1])] = 0;


            case _:
            
                print ("Time %s  Reply %s" %(time.time(), arduinoReply))
                file.write(arduinoReply + "\n")

                sendToArduino("asleep")
                sendToArduino("fire")

                os.system("python3 ~/LLMs/PLLantoid/v2/speak_now.py");

                sendToArduino("fire")
                sendToArduino("awake")




    # os.system("python3 ~//LLMs/PLLantoid/haiku.py")

       # serialPort.write('c')

       # data = serialPort.read()

        # if data:
        #     print(data)

        #     serialPort.write(b'd')
        #     print("sentt")




         # send a message at intervals
    #  if time.time() - prevTime > 10.0:
    #      print ("CHANGING MODE.....")
    #      sendToArduino("food")
    #      prevTime = time.time()
    #      count += 1