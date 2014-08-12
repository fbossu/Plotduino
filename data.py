import random
import glob
import serial
from serial.tools.list_ports import *
import time
from threading import Thread

"""
Thanks to: gregpinero
Snap of code taken from ArduinoPlot:
https://github.com/gregpinero/ArduinoPlot
"""
stopthread = False
last_received = ''
def receiving(ser):
    global last_received
    global stopthread
    buffer = ''
    while True:
        buffer = buffer + ser.read(ser.inWaiting())
        if '\n' in buffer:
            lines = buffer.split('\n') # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]
        time.sleep(0.01)
        if stopthread:
          break
"""
========================================
========================================
"""

class data():
  def __init__(self):
    self.x = []
    self.y = []
    self.t = 0
    random.seed(0)
    
    self.selection = 0
    self.serialport = ""
    self.si = serialInterface()

  def setPortName(self, name):
    self.si.port_name = name
    
  def getdata(self, N ):  
    valstr = last_received.split(',')
    valnum = []
    if not self.si.datataking:
      self.si.openserial()

    if not self.si.datataking and self.si.port_name != "Test":
        time.sleep(0.5)
        self.si.daqStart()
    
    if self.si.port_name == "Test":
      for iv in range(0,N):
        valnum.append( random.random() )
    elif len(valstr) < N:
      for iv in range(0,N):
        valnum.append( 0 )
        print "*** WARNING ***, the received string contains less fields than requested"
        
    else:
      for iv in range(0,N):
        tmpv = 0
        try:
          tmpv = float(valstr[iv].strip())
        except:
          print "*** WARNING ***, corrupted data ", valstr[iv]
        valnum.append( tmpv  )
        
    self.si.datataking = True
    return valnum
  
  def __del__(self):
    del self.si


"""===============================
Interface to the arduino

==================================="""  
class serialInterface():
  def __init__(self):
    self.port_name = 'Test'
    self.names = self.getListOfSerialPorts()
    self.bitrate = 9600
    self.bitrates = ['4800', '9600', '14400', '28800', '57600', '115200' ]
    self.request_char = ''
    self.datataking = False
     
  def openserial(self):
    print "opening serial communication...", unicode(self.port_name), self.bitrate
    try:
      self.ser = serial.Serial(
                port=unicode(self.port_name),
                baudrate=self.bitrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1,
                xonxoff=0,
                rtscts=0,
                interCharTimeout=None
            )

    except:
      print "**** ERROR opening the serial port. Falling back to Test mode ***"
      self.port_name = 'Test'
    else:
      if self.ser.isOpen() is True:
        print "Serial communcation open.", " Serial port: ", self.port_name
      else:
        print "Problems opening the serial communication, falling back to Test mode"
        self.port_name = 'Test'

  def daqStart(self):
    global stopthread
    stopthread = False
    self.ser.write('a')  # caracter needed to exit the setup function
    time.sleep(0.5)
    Thread(target=receiving, args=(self.ser,)).start()
    
  def daqStop(self):
    global stopthread
    stopthread = True
    
  def getListOfSerialPorts( self ):
    l = sorted(comports())  # from serial.tools
    s = [ self.port_name ]
    for i in l: s.append( i[0] )
    
    return s
    
  def __del__(self):
    try:
      self.daqStop()
      self.ser.close()
    except:
      pass
  
