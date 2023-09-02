import serial
import time
import os, signal
import random
import regex_spm
from multiprocessing import Process
import subprocess
import threading

startMarker = '<'
endMarker = '>'
dataStarted = False
dataBuf = ""
messageComplete = False

def setupSerial(baudRate, serialPortName):

    global  serialPort

    serialPort = serial.Serial(port= serialPortName, baudrate = baudRate)

    print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))

    waitForArduino(serialPort)

def sendToArduino(stringToSend):

        # this adds the start- and end-markers before sending
    global startMarker, endMarker, serialPort

    stringWithMarkers = (startMarker)
    stringWithMarkers += stringToSend
    stringWithMarkers += (endMarker)

    serialPort.write(stringWithMarkers.encode('utf-8')) # encode needed for Python3

def recvLikeArduino():

    global startMarker, endMarker, serialPort, dataStarted, dataBuf, messageComplete

    if serialPort.inWaiting() > 0 and messageComplete == False:

        x = ""

        try:
            x = serialPort.read().decode("utf-8") # decode needed for Python3
        except UnicodeDecodeError: print('Serial error\n');

        if x:
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

def waitForArduino(serialPort):
    """
    Waits for the Arduino to send a custom init message.
    
    Parameters:
    - serialPort: The serial port object associated with the Arduino.
    
    Returns:
    - Dictionary mapping serial ports to device serial numbers.
    """

    # serialPort.write("AT+RST".encode('utf-8'))
    serialPort.setDTR(False)
    time.sleep(1)
    serialPort.flushInput()
    serialPort.setDTR(True)
 

    print("Waiting for Arduino to send init message")

    # Read data from the serial port
    # data = serialPort.readline().decode().strip()

    # # Dictionary to store the association between the serial port and the device serial number
    # devices_dict = {}

    # # Check if the data received starts with 'Init:'
    # if data.startswith('Init:'):
    #     serial_number = data.split(':')[1]   # Extract the serial number
    #     devices_dict[serialPort] = serial_number

    # return devices_dict
    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == 'XXX'):
            print(msg)
