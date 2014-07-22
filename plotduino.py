#!/usr/bin/env python
# main file. 
#
import sys, glib
from PyQt4 import QtGui, QtCore

#import my libraries
import mtp, data

class MainWin(QtGui.QMainWindow):
  def __init__( self, parent=None ):
    QtGui.QMainWindow.__init__( self, parent )
    self.setWindowTitle( 'Plotduino' )
    
    # the data acquisition
    self.data_source = data.data()
    self.data_source.selection = 0
    
    # timer for updating the plot
    self.timer = QtCore.QTimer(self)

    #create the layout and connect the signals to the buttons
    self.set_layout()
    self.connectSignals()

  def set_layout( self ):
    """ definistion of the window layout """
    self.main_frame = QtGui.QWidget()
    #self.main_frame.setFixedHeight(500)
    
    self.plot = mtp.mtp( self.main_frame )
    
  
    #actual layout 
    #******************
    
    # layout left:
    #-------------
    vboxleft = QtGui.QVBoxLayout()
    
    # the matplotlib canvas
    vboxleft.addWidget(self.plot.canvas)    
 
    # the play and stop button
    hbox = QtGui.QHBoxLayout()
    self.play_button = QtGui.QPushButton("&Play")
    hbox.addWidget(self.play_button)
    self.stop_button = QtGui.QPushButton("&Stop")
    hbox.addWidget(self.stop_button)
    vboxleft.addLayout(hbox)

    #layout right:
    #------------

    # Serial port configuration
    self.select_serial_box = QtGui.QComboBox()
    self.select_serial_box.addItems( self.data_source.si.getListOfSerialPorts() )
    
  
    # Configuration of the output plot
    self.plotname_box = QtGui.QComboBox()
    self.plotname_box.addItems( self.plot.plotnames )
    

    # Close button
    self.close_button = QtGui.QPushButton("&Close")
    
    
    vboxright = QtGui.QVBoxLayout()
    vboxright.addWidget(self.select_serial_box)
    vboxright.addWidget(self.plotname_box)
    
    vboxright.addItem(QtGui.QSpacerItem(20,40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
    
    vboxright.addWidget(self.close_button)
    
    
    # Global horizontal layout: takes the two vertial box layouts
    hboxmain = QtGui.QHBoxLayout()
    hboxmain.addLayout(vboxleft)
    hboxmain.addLayout(vboxright)
    
    # setting the global horizontal box as the main_frame layout
    self.main_frame.setLayout( hboxmain )
    self.setCentralWidget( self.main_frame )
    
    
  def connectSignals(self):
    """ """
    self.connect(self.play_button, QtCore.SIGNAL('clicked()'), self.play)
    self.connect(self.stop_button, QtCore.SIGNAL('clicked()'), self.stop)
    self.connect(self.close_button, QtCore.SIGNAL('clicked()'), self.close)
    self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.draw)
    

  def start_serial( self ):
    self.data_source.setPortName(self.select_serial_box.currentText())

  def play(self):
    self.plot.plotkind = self.plotname_box.currentText()
    self.plot.importdata( self.data_source )
    self.start_serial()
    self.timer.start(200)
    self.play_button.setDown(True)
    self.play_button.setEnabled(False)
    self.stop_button.setEnabled(True)
    self.select_serial_box.setEnabled(False)
    self.plotname_box.setEnabled(False)
     
  def stop( self ):
    self.data_source.si.daqStop()
    self.timer.stop()
    self.play_button.setEnabled(True)
    self.stop_button.setEnabled(False)
    
  def draw(self):
    self.plot.updateplot()
    
  def __del__(self):
    del self.data_source
    del self.plot


#------------------------------------------------------------------    
def main():
  #start Qt the Qt application
  app = QtGui.QApplication(sys.argv)
  
  #create and draw the main window
  w = MainWin() 
  w.show()

  #exit when the window is closed 
  sys.exit(app.exec_())

if __name__ == '__main__':
    main()
